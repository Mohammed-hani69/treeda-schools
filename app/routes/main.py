from flask import Blueprint, render_template, abort, current_app, redirect, url_for, session, request, flash
from flask_mail import Message
from app import db, mail
from app.models.home import HeroSection
from app.models.category import Category
from app.models.school import School
from app.models.plan import Plan
from app.models.user import User
from app.models.notification import Notification
from app.models.setting import Setting
from app.utils.translations import _ as _tr
from sqlalchemy import desc

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    hero = HeroSection.query.filter_by(is_active=True).first()
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    featured_schools = School.query.filter_by(is_featured=True, is_approved=True, is_active=True)\
        .order_by(desc(School.views)).limit(6).all()
    plans = Plan.query.filter_by(is_active=True).order_by(Plan.sort_order).all()
    return render_template('main/index.html',
                         hero=hero,
                         categories=categories,
                         featured_schools=featured_schools,
                         plans=plans)


@main_bp.route('/lang/<lang>')
def set_lang(lang):
    if lang in ('en', 'ar'):
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))


@main_bp.route('/about')
def about():
    return render_template('main/about.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    lang = session.get('lang', 'ar')
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash(_tr('contact.sent_error', lang), 'danger')
            return redirect(url_for('main.contact'))

        body = f'''
رسالة جديدة من نموذج الاتصال
─────────────────────────────
الاسم: {name}
البريد: {email}
الموضوع: {subject or '(بدون موضوع)'}

الرسالة:
{message}
'''

        try:
            setting = Setting.query.first()
            admin = User.query.filter_by(role='admin').first()

            # Send email
            msg = Message(
                subject=f'اتصال جديد: {subject or "بدون عنوان"}',
                recipients=[setting.contact_email] if setting and setting.contact_email else [admin.email],
                body=body
            )
            mail.send(msg)

            # Create notification for admin
            if admin:
                notif = Notification(
                    user_id=admin.id,
                    title='رسالة اتصال جديدة',
                    message=f'من {name} ({email}): {message[:100]}',
                    notification_type='admin_message',
                )
                db.session.add(notif)
                db.session.commit()

            flash(_tr('contact.sent_ok', lang), 'success')
        except Exception as e:
            current_app.logger.error(f'Contact form error: {e}')
            flash(_tr('contact.sent_error', lang), 'danger')

        return redirect(url_for('main.contact'))

    return render_template('main/contact.html')


@main_bp.route('/category/<slug>')
def category_detail(slug):
    category = Category.query.filter_by(slug=slug, is_active=True).first_or_404()
    type_map = {
        'government-schools': 'government',
        'private-schools': 'private',
        'international-schools': 'international',
        'quran-schools': 'quran',
    }
    school_type = type_map.get(slug)
    schools = School.query.filter_by(
        school_type=school_type, is_approved=True, is_active=True
    ).order_by(School.is_featured.desc(), School.name).all()
    return render_template('main/category.html', category=category, schools=schools)


@main_bp.route('/school/<slug>')
def school_detail(slug):
    school = School.query.filter_by(slug=slug, is_active=True, is_approved=True).first_or_404()
    from app.models.school import SchoolMedia
    images = school.approved_media('image').order_by(SchoolMedia.created_at.desc()).all()
    videos = school.approved_media('video').order_by(SchoolMedia.created_at.desc()).all()
    return render_template('parent/school_detail.html',
                         school=school, images=images, videos=videos)


@main_bp.route('/plans')
def plans():
    plans = Plan.query.filter_by(is_active=True).order_by(Plan.sort_order).all()
    return render_template('main/plans.html', plans=plans)
