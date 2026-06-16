from flask import Blueprint, render_template, abort, current_app, redirect, url_for, session, request, flash
from flask_mail import Message
from app import db, mail
from app.models.home import HeroSection
from app.models.category import Category
from app.models.school import School, SchoolVisitLog
from app.models.plan import Plan
from app.models.user import User
from app.models.notification import Notification
from app.models.setting import Setting
from app.models.contact_message import ContactMessage
from app.utils.translations import _ as _tr
from sqlalchemy import desc

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    hero = HeroSection.query.filter_by(is_active=True).first()
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    recommended_schools = School.query.filter_by(is_featured=True, is_approved=True, is_active=True)\
        .order_by(desc(School.views)).limit(12).all()
    return render_template('main/index.html',
                         hero=hero,
                         categories=categories,
                         recommended_schools=recommended_schools)


@main_bp.route('/lang/<lang>')
def set_lang(lang):
    if lang in ('en', 'ar'):
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))


@main_bp.route('/about')
def about():
    from app.models.school import School
    from app.models.parent import Parent
    from sqlalchemy import func

    stats = {
        'schools': School.query.filter_by(is_approved=True, is_active=True).count(),
        'parents': Parent.query.count(),
        'views': db.session.query(func.coalesce(func.sum(School.views), 0)).scalar() or 0,
    }
    return render_template('main/about.html', stats=stats)


@main_bp.route('/contact-message', methods=['POST'])
def contact_message():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not email or not message:
        flash('يرجى ملء جميع الحقول', 'danger')
        return redirect(request.referrer or url_for('main.index'))

    try:
        msg = ContactMessage(name=name, email=email, message=message)
        db.session.add(msg)
        db.session.commit()

        admin = User.query.filter_by(role='admin').first()
        if admin:
            notif = Notification(
                user_id=admin.id,
                title='رسالة جديدة من الموقع',
                message=f'من {name} ({email}): {message[:100]}',
                notification_type='admin_message',
            )
            db.session.add(notif)
            db.session.commit()

        flash('تم إرسال رسالتك بنجاح', 'success')
    except Exception as e:
        current_app.logger.error(f'Contact message error: {e}')
        flash('حدث خطأ أثناء الإرسال', 'danger')

    return redirect(request.referrer or url_for('main.index'))


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
    schools = School.query.filter(
        db.or_(
            School.category_id == category.id,
            School.school_type == school_type if school_type else False
        ),
        School.is_approved == True,
        School.is_active == True
    ).order_by(School.is_featured.desc(), School.name).all()
    return render_template('main/category.html', category=category, schools=schools)


@main_bp.route('/school/<slug>')
def school_detail(slug):
    school = School.query.filter_by(slug=slug, is_active=True, is_approved=True).first_or_404()
    school.views = (school.views or 0) + 1
    SchoolVisitLog.record_visit(school.id)
    db.session.commit()
    from app.models.school import SchoolMedia
    images = school.approved_media('image').order_by(SchoolMedia.created_at.desc()).all()
    videos = school.approved_media('video').order_by(SchoolMedia.created_at.desc()).all()
    return render_template('parent/school_detail.html',
                         school=school, images=images, videos=videos)


@main_bp.route('/pricing')
@main_bp.route('/plans')
def plans():
    plans = Plan.query.filter_by(is_active=True).order_by(Plan.sort_order).all()
    return render_template('main/plans.html', plans=plans)


@main_bp.route('/payment/<int:plan_id>')
def payment(plan_id):
    plan = Plan.query.get_or_404(plan_id)
    setting = Setting.query.first()
    return render_template('main/payment.html', plan=plan, setting=setting)
