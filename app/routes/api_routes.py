import re
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db, csrf
from app.models.school import School, SchoolMedia
from app.models.notification import Notification
from app.models.ai_knowledge import AiKnowledge
from app.utils.translations import _ as _t

api_bp = Blueprint('api', __name__)


@api_bp.route('/notifications/count')
@login_required
def notification_count():
    count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return jsonify({'count': count})


@api_bp.route('/notifications')
@login_required
def notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id)\
        .order_by(Notification.created_at.desc()).limit(10).all()
    return jsonify([{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'type': n.notification_type,
        'link': n.link,
        'is_read': n.is_read,
        'created_at': n.created_at.isoformat() if n.created_at else None
    } for n in notifs])


@api_bp.route('/schools/search')
def search_schools():
    q = request.args.get('q', '')
    if len(q) < 2:
        return jsonify([])
    schools = School.query.filter(
        School.is_approved == True,
        School.is_active == True,
        School.name.ilike(f'%{q}%')
    ).limit(10).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'slug': s.slug,
        'city': s.city,
        'logo': s.logo
    } for s in schools])


@api_bp.route('/settings/theme', methods=['POST'])
@login_required
def update_theme():
    data = request.get_json()
    theme = data.get('theme', 'light')
    from app.models.setting import Setting
    setting = Setting.query.first()
    if setting:
        setting.theme = theme
        db.session.commit()
        return jsonify({'success': True, 'theme': theme})
    return jsonify({'error': 'Settings not found'}), 404


@api_bp.route('/home/sections/reorder', methods=['POST'])
@login_required
def reorder_sections():
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    if data and 'order' in data:
        from app.models.home import HomeSection
        for item in data['order']:
            section = HomeSection.query.get(item['id'])
            if section:
                section.sort_order = item['order']
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid data'}), 400


def _norm_arabic(text):
    """Normalize Arabic: unify alef, teh marbuta → heh, remove tashkeel."""
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    text = text.replace('ة', 'ه')
    text = re.sub(r'[ًٌٍَُِّْ]', '', text)
    return text

def _words(text):
    """Split text into lowercase word tokens."""
    return re.findall(r'[\w]+', text.lower())

def _affix_strip(word):
    """Crude Arabic affix stripping to approximate a root (min 3 chars result)."""
    if len(word) < 4:
        return word
    stripped = word
    # Definite article
    if stripped.startswith('ال') and len(stripped) > 5:
        stripped = stripped[2:]
    # Common prefixes (sorted longest first; uses bare alef ا after _norm_arabic normalization)
    for p in ['فب', 'فل', 'فس', 'وب', 'لل', 'سا', 'سن', 'سي', 'ست',
              'ف', 'ب', 'ل', 'ك', 'و', 'س', 'ا', 'ي', 'ت', 'ن']:
        if stripped.startswith(p) and len(stripped) - len(p) >= 3:
            stripped = stripped[len(p):]
            break
    # Common suffixes (sorted longest first)
    for s in ['هما', 'كما', 'نتم', 'نكن', 'كما', 'ون', 'ين', 'ان', 'ات',
              'تم', 'تن', 'نا', 'ها', 'هم', 'هن', 'كم', 'كن',
              'ني', 'تو', 'وا', 'ته', 'تا', 'تي', 'ت', 'ي', 'ه', 'ة', 'ا', 'ن']:
        if stripped.endswith(s) and len(stripped) - len(s) >= 3:
            stripped = stripped[:-len(s)]
            break
    return stripped if len(stripped) >= 3 else word

def _score_item(keywords_list, msg_lower, msg_words, msg_norm, msg_words_norm, msg_words_root):
    """Multi-strategy keyword matching score for one knowledge item.
    
    Tracks which user message words have already contributed to avoid
    the same word inflating scores across multiple similar keywords.
    Each unique keyword word → user word pair contributes at most 1.
    """
    total = 0
    used_msg_words = set()

    for kw in keywords_list:
        kw_norm = _norm_arabic(kw)
        kw_words = _words(kw)
        matched = False

        # ── Strategy 1: Full keyword substring (original) ──
        if kw in msg_lower:
            # Mark all user words as used since the entire keyword matches
            used_msg_words.update(msg_words)
            total += 1
            continue

        # ── Strategy 2: Normalized keyword substring ──
        if kw_norm in msg_norm:
            used_msg_words.update(msg_words)
            total += 1
            continue

        # ── Strategy 3: Word-level containment ──
        for kww in kw_words:
            if len(kww) < 3:
                continue
            for mw in msg_words:
                if mw in used_msg_words:
                    continue
                if kww in mw or mw in kww:
                    used_msg_words.add(mw)
                    total += 1
                    matched = True
                    break
            if matched:
                break
        if matched:
            continue

        # ── Strategy 4: Root overlap ──
        for kww in kw_words:
            if len(kww) < 4:
                continue
            kww_root = _affix_strip(_norm_arabic(kww))
            if len(kww_root) < 3:
                continue
            for i, mw_root in enumerate(msg_words_root):
                if msg_words[i] in used_msg_words:
                    continue
                if len(mw_root) < 3:
                    continue
                # Contiguous substring match
                if kww_root in mw_root or mw_root in kww_root:
                    used_msg_words.add(msg_words[i])
                    total += 1
                    matched = True
                    break
                # Character-set overlap for non-consecutive Arabic roots
                k_set = set(kww_root)
                m_set = set(mw_root)
                common = len(k_set & m_set)
                if common >= 3:
                    overlap = common / max(len(k_set), len(m_set))
                    if overlap >= 0.65:
                        used_msg_words.add(msg_words[i])
                        total += 1
                        matched = True
                        break
            if matched:
                break

    return total


@api_bp.route('/chat', methods=['POST'])
@csrf.exempt
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'answer': None}), 200

    msg = data['message'].strip().lower()
    lang = data.get('lang', 'ar')
    if not msg:
        return jsonify({'answer': None}), 200

    # Pre-process message once
    msg_words = _words(msg)
    msg_norm = _norm_arabic(msg)
    msg_words_norm = [_norm_arabic(w) for w in msg_words]
    msg_words_root = [_affix_strip(w) for w in msg_words_norm]

    items = AiKnowledge.query.filter_by(is_active=True).order_by(AiKnowledge.sort_order).all()
    best_match = None
    best_score = 0

    for item in items:
        score = _score_item(item.get_keywords_list(), msg, msg_words,
                           msg_norm, msg_words_norm, msg_words_root)
        if score > best_score:
            best_score = score
            best_match = item

    if best_match and best_score > 0:
        answer = best_match.answer_en if lang == 'en' else best_match.answer_ar
        return jsonify({'answer': answer, 'fallback': False})

    fallback = _t('chat.fallback', lang)
    return jsonify({'answer': fallback, 'fallback': True})
