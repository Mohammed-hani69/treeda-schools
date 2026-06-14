from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db, csrf
from app.models.school import School, SchoolMedia
from app.models.notification import Notification
from app.models.ai_knowledge import AiKnowledge

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

    items = AiKnowledge.query.filter_by(is_active=True).order_by(AiKnowledge.sort_order).all()
    best_match = None
    best_count = 0

    for item in items:
        keywords = item.get_keywords_list()
        match_count = sum(1 for kw in keywords if kw in msg)
        if match_count > best_count:
            best_count = match_count
            best_match = item

    if best_match and best_count > 0:
        answer = best_match.answer_en if lang == 'en' else best_match.answer_ar
        return jsonify({'answer': answer})

    return jsonify({'answer': None})
