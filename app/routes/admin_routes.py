from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.school import School, SchoolMedia, SchoolActivity, SchoolService, SchoolGrade
from app.models.parent import Parent
from app.models.plan import Plan, Subscription
from app.models.category import Category
from app.models.home import HeroSection
from app.models.home_content import Feature, Stat, GalleryItem, Step, Testimonial, FaqItem
from app.models.notification import Notification
from app.models.payment import Payment
from app.models.setting import Setting
from app.models.ai_knowledge import AiKnowledge
from app.utils.decorators import admin_required
from app.utils.helpers import save_file, delete_file, allowed_file, generate_slug
from app.forms.admin_forms import (PlanForm, CategoryForm, HeroSectionForm, AdminSchoolCreateForm,
    FeatureForm, StatForm, GalleryItemForm, StepForm, TestimonialForm, FaqItemForm, SchoolEditForm)
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import json
import os

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request
def check_admin():
    if current_user.is_authenticated and not current_user.is_admin():
        flash('غير مصرح بالدخول', 'danger')
        return redirect(url_for('main.index'))


@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_schools = School.query.count()
    total_parents = Parent.query.count()
    total_plans = Plan.query.count()
    total_subscriptions = Subscription.query.count()
    total_images = SchoolMedia.query.filter_by(media_type='image').count()
    total_videos = SchoolMedia.query.filter_by(media_type='video').count()
    featured_schools = School.query.filter_by(is_featured=True).count()
    pending_media = SchoolMedia.query.filter_by(status='pending').count()
    pending_schools = School.query.filter_by(is_approved=False).count()

    recent_schools = School.query.order_by(desc(School.created_at)).limit(5).all()
    recent_parents = Parent.query.order_by(desc(Parent.created_at)).limit(5).all()

    from sqlalchemy import text as sa_text
    db_url = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if 'sqlite' in db_url:
        date_func = func.strftime('%Y-%m', Subscription.created_at)
    else:
        date_func = func.date_format(Subscription.created_at, '%%Y-%%m')
    subscriptions_by_month = db.session.query(
        date_func.label('month'),
        func.count(Subscription.id).label('count')
    ).group_by('month').order_by('month').limit(12).all()

    schools_by_type = db.session.query(
        School.school_type, func.count(School.id)
    ).filter(School.school_type.isnot(None), School.school_type != '').group_by(School.school_type).all()

    return render_template('admin/dashboard.html',
        total_schools=total_schools,
        total_parents=total_parents,
        total_plans=total_plans,
        total_subscriptions=total_subscriptions,
        total_images=total_images,
        total_videos=total_videos,
        featured_schools=featured_schools,
        pending_media=pending_media,
        pending_schools=pending_schools,
        recent_schools=recent_schools,
        recent_parents=recent_parents,
        subscriptions_by_month=json.dumps([{'month': s[0], 'count': s[1]} for s in subscriptions_by_month]),
        schools_by_type=json.dumps([{'type': s[0], 'count': s[1]} for s in schools_by_type]))


@admin_bp.route('/schools')
@login_required
@admin_required
def schools():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    search = request.args.get('search', '')

    query = School.query
    if status == 'pending':
        query = query.filter_by(is_approved=False)
    elif status == 'approved':
        query = query.filter_by(is_approved=True)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)
    if search:
        query = query.filter(School.name.ilike(f'%{search}%'))

    schools = query.order_by(desc(School.created_at)).paginate(page=page, per_page=20)
    return render_template('admin/schools.html', schools=schools, status=status, search=search)


@admin_bp.route('/schools/approve/<int:id>', methods=['POST'])
@login_required
@admin_required
def approve_school(id):
    school = School.query.get_or_404(id)
    school.is_approved = True
    user = User.query.get(school.user_id)
    if user:
        notif = Notification(
            user_id=user.id,
            title='تم قبول حساب المدرسة',
            message=f'تم قبول حساب مدرسة {school.name} يمكنك الآن تسجيل الدخول وإدارة ملفك',
            notification_type='content_approved',
            link=url_for('school.dashboard')
        )
        db.session.add(notif)
    db.session.commit()
    flash(f'تم قبول مدرسة {school.name}', 'success')
    return redirect(url_for('admin.schools'))


@admin_bp.route('/schools/reject/<int:id>', methods=['POST'])
@login_required
@admin_required
def reject_school(id):
    school = School.query.get_or_404(id)
    reason = request.form.get('reason', '')
    user = User.query.get(school.user_id)
    if user:
        notif = Notification(
            user_id=user.id,
            title='تم رفض حساب المدرسة',
            message=f'عذراً، تم رفض حساب مدرسة {school.name}. السبب: {reason}',
            notification_type='content_rejected',
        )
        db.session.add(notif)
    db.session.delete(school)
    db.session.delete(user)
    db.session.commit()
    flash('تم رفض المدرسة', 'success')
    return redirect(url_for('admin.schools'))


@admin_bp.route('/schools/toggle/<int:id>', methods=['POST'])
@login_required
@admin_required
def toggle_school(id):
    school = School.query.get_or_404(id)
    school.is_active = not school.is_active
    db.session.commit()
    status = 'تفعيل' if school.is_active else 'إيقاف'
    flash(f'تم {status} المدرسة', 'success')
    return redirect(url_for('admin.schools'))


@admin_bp.route('/schools/feature/<int:id>', methods=['POST'])
@login_required
@admin_required
def feature_school(id):
    school = School.query.get_or_404(id)
    school.is_featured = not school.is_featured
    db.session.commit()
    flash('تم تعديل حالة التميز', 'success')
    return redirect(url_for('admin.schools'))


@admin_bp.route('/schools/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_school(id):
    school = School.query.get_or_404(id)
    name = school.name
    user = User.query.get(school.user_id)
    db.session.delete(school)
    if user:
        db.session.delete(user)
    db.session.commit()
    flash(f'تم حذف مدرسة {name} نهائياً', 'success')
    return redirect(url_for('admin.schools'))


@admin_bp.route('/schools/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_school():
    from app.models.category import Category
    form = AdminSchoolCreateForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(is_active=True).order_by(Category.name).all()]
    if not form.category_id.choices:
        form.category_id.choices = [(0, '— لا توجد أقسام —')]

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('البريد الإلكتروني مستخدم بالفعل', 'danger')
            return render_template('admin/school_form.html', form=form, title='إضافة مدرسة جديدة')
        if User.query.filter_by(username=form.username.data).first():
            flash('اسم المستخدم مستخدم بالفعل', 'danger')
            return render_template('admin/school_form.html', form=form, title='إضافة مدرسة جديدة')

        user = User(
            username=form.username.data,
            email=form.email.data,
            role='school',
            is_active=True,
            is_verified=True
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        logo_filename = save_file(form.logo.data, 'schools') if form.logo.data else None
        cover_filename = save_file(form.cover.data, 'schools') if form.cover.data else None
        image_filename = save_file(form.image.data, 'schools') if form.image.data else None

        category_id = form.category_id.data if form.category_id.data and form.category_id.data > 0 else None

        school = School(
            user_id=user.id,
            name=form.name.data,
            slug=generate_slug(form.name.data, School),
            about=form.about.data,
            address=form.address.data,
            city=form.city.data,
            district=form.district.data,
            phone=form.phone.data,
            email=form.email.data,
            website=form.website.data,
            category_id=category_id,
            gender=form.gender.data or None,
            logo=logo_filename,
            cover=cover_filename,
            image=image_filename,
            is_approved=True,
            is_active=True
        )
        db.session.add(school)
        db.session.commit()
        flash(f'تم إنشاء مدرسة {school.name} بنجاح', 'success')
        return redirect(url_for('admin.schools'))

    return render_template('admin/school_form.html', form=form, title='إضافة مدرسة جديدة')


@admin_bp.route('/schools/views/<int:id>', methods=['POST'])
@login_required
@admin_required
def update_school_views(id):
    school = School.query.get_or_404(id)
    try:
        new_views = int(request.form.get('views', 0))
        school.views = max(0, new_views)
        db.session.commit()
        flash(f'تم تحديث عدد الزيارات لمدرسة {school.name} إلى {school.views}', 'success')
    except (ValueError, TypeError):
        flash('قيمة غير صالحة', 'danger')
    return redirect(url_for('admin.schools'))


@admin_bp.route('/media')
@login_required
@admin_required
def media():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pending')
    media_type = request.args.get('type', 'all')

    query = SchoolMedia.query
    if status != 'all':
        query = query.filter_by(status=status)
    if media_type != 'all':
        query = query.filter_by(media_type=media_type)

    media_list = query.order_by(desc(SchoolMedia.created_at)).paginate(page=page, per_page=30)
    return render_template('admin/media.html', media=media_list, status=status, media_type=media_type)


@admin_bp.route('/media/approve/<int:id>', methods=['POST'])
@login_required
@admin_required
def approve_media(id):
    media_item = SchoolMedia.query.get_or_404(id)
    media_item.status = 'approved'
    school = School.query.get(media_item.school_id)
    if school:
        user = User.query.get(school.user_id)
        if user:
            notif = Notification(
                user_id=user.id,
                title='تم قبول المحتوى',
                message=f'تم قبول {media_item.original_name or media_item.filename}',
                notification_type='content_approved',
                link=url_for('school.media')
            )
            db.session.add(notif)
    db.session.commit()
    flash('تم قبول المحتوى', 'success')
    return redirect(url_for('admin.media'))


@admin_bp.route('/media/reject/<int:id>', methods=['POST'])
@login_required
@admin_required
def reject_media(id):
    media_item = SchoolMedia.query.get_or_404(id)
    reason = request.form.get('reason', '')
    media_item.status = 'rejected'
    media_item.rejection_reason = reason
    school = School.query.get(media_item.school_id)
    if school:
        user = User.query.get(school.user_id)
        if user:
            notif = Notification(
                user_id=user.id,
                title='تم رفض المحتوى',
                message=f'تم رفض {media_item.original_name or media_item.filename}. السبب: {reason}',
                notification_type='content_rejected',
                link=url_for('school.media')
            )
            db.session.add(notif)
    db.session.commit()
    flash('تم رفض المحتوى', 'success')
    return redirect(url_for('admin.media'))


@admin_bp.route('/media/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_media(id):
    media_item = SchoolMedia.query.get_or_404(id)
    delete_file(media_item.filename, 'media')
    db.session.delete(media_item)
    db.session.commit()
    flash('تم حذف المحتوى', 'success')
    return redirect(url_for('admin.media'))


@admin_bp.route('/parents')
@login_required
@admin_required
def parents():
    page = request.args.get('page', 1, type=int)
    parents = Parent.query.order_by(desc(Parent.created_at)).paginate(page=page, per_page=20)
    return render_template('admin/parents.html', parents=parents)


@admin_bp.route('/parents/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_parent(id):
    parent = Parent.query.get_or_404(id)
    user = User.query.get(parent.user_id)
    db.session.delete(parent)
    if user:
        db.session.delete(user)
    db.session.commit()
    flash('تم حذف ولي الأمر', 'success')
    return redirect(url_for('admin.parents'))


@admin_bp.route('/plans')
@login_required
@admin_required
def plans():
    plans = Plan.query.order_by(Plan.sort_order).all()
    return render_template('admin/plans.html', plans=plans)


@admin_bp.route('/plans/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_plan():
    form = PlanForm()
    if form.validate_on_submit():
        plan = Plan(
            name=form.name.data,
            name_en=form.name_en.data,
            description=form.description.data,
            price=form.price.data,
            currency=form.currency.data,
            duration_days=form.duration_days.data,
            max_images=form.max_images.data,
            max_videos=form.max_videos.data,
            storage_mb=form.storage_mb.data,
            max_employees=form.max_employees.data,
            is_featured=form.is_featured.data,
            color=form.color.data,
            sort_order=form.sort_order.data,
            is_active=form.is_active.data,
            features=form.features.data
        )
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            filename = save_file(form.image.data, 'plans')
            if filename:
                plan.image = filename
        db.session.add(plan)
        db.session.commit()
        flash('تم إنشاء الباقة بنجاح', 'success')
        return redirect(url_for('admin.plans'))
    return render_template('admin/plan_form.html', form=form, title='إضافة باقة جديدة')


@admin_bp.route('/plans/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_plan(id):
    plan = Plan.query.get_or_404(id)
    form = PlanForm(obj=plan)
    if form.validate_on_submit():
        old_image = plan.image
        form.populate_obj(plan)
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            filename = save_file(form.image.data, 'plans')
            if filename:
                plan.image = filename
                if old_image:
                    delete_file(old_image, 'plans')
        else:
            plan.image = old_image
        db.session.commit()
        flash('تم تحديث الباقة', 'success')
        return redirect(url_for('admin.plans'))
    return render_template('admin/plan_form.html', form=form, title='تعديل الباقة', plan=plan)


@admin_bp.route('/plans/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_plan(id):
    plan = Plan.query.get_or_404(id)
    if plan.image:
        delete_file(plan.image, 'plans')
    db.session.delete(plan)
    db.session.commit()
    flash('تم حذف الباقة', 'success')
    return redirect(url_for('admin.plans'))


@admin_bp.route('/subscriptions')
@login_required
@admin_required
def subscriptions():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    query = Subscription.query
    if status != 'all':
        query = query.filter_by(status=status)
    subscriptions = query.order_by(desc(Subscription.created_at)).paginate(page=page, per_page=20)
    return render_template('admin/subscriptions.html', subscriptions=subscriptions, status=status)


@admin_bp.route('/subscriptions/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_subscription():
    from app.forms.admin_forms import SubscriptionForm

    form = SubscriptionForm()
    form.school_id.choices = [(s.id, s.name) for s in School.query.order_by(School.name).all()]
    form.plan_id.choices = [(p.id, p.name) for p in Plan.query.filter_by(is_active=True).order_by(Plan.sort_order).all()]

    if form.validate_on_submit():
        existing = Subscription.query.filter_by(school_id=form.school_id.data).first()
        if existing:
            flash('هذه المدرسة لديها اشتراك بالفعل. يمكنك تعديله.', 'warning')
            return redirect(url_for('admin.edit_subscription', id=existing.id))
        sub = Subscription(
            school_id=form.school_id.data,
            plan_id=form.plan_id.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status=form.status.data,
            auto_renew=form.auto_renew.data,
            price_paid=form.price_paid.data,
        )
        db.session.add(sub)
        db.session.commit()
        flash('تم إنشاء الاشتراك بنجاح', 'success')
        return redirect(url_for('admin.subscriptions'))
    return render_template('admin/subscription_form.html', form=form, title='إضافة اشتراك')


@admin_bp.route('/subscriptions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_subscription(id):
    from app.forms.admin_forms import SubscriptionForm

    sub = Subscription.query.get_or_404(id)
    form = SubscriptionForm(obj=sub)
    form.school_id.choices = [(s.id, s.name) for s in School.query.order_by(School.name).all()]
    form.plan_id.choices = [(p.id, p.name) for p in Plan.query.filter_by(is_active=True).order_by(Plan.sort_order).all()]

    if form.validate_on_submit():
        form.populate_obj(sub)
        db.session.commit()
        flash('تم تحديث الاشتراك', 'success')
        return redirect(url_for('admin.subscriptions'))
    return render_template('admin/subscription_form.html', form=form, title='تعديل الاشتراك', sub=sub)


@admin_bp.route('/subscriptions/toggle/<int:id>', methods=['POST'])
@login_required
@admin_required
def toggle_subscription(id):
    sub = Subscription.query.get_or_404(id)
    sub.status = 'active' if sub.status == 'inactive' else 'inactive'
    db.session.commit()
    flash('تم تحديث حالة الاشتراك', 'success')
    return redirect(url_for('admin.subscriptions'))


@admin_bp.route('/subscriptions/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_subscription(id):
    sub = Subscription.query.get_or_404(id)
    db.session.delete(sub)
    db.session.commit()
    flash('تم حذف الاشتراك', 'success')
    return redirect(url_for('admin.subscriptions'))


@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    categories = Category.query.order_by(Category.sort_order).all()
    return render_template('admin/categories.html', categories=categories)


@admin_bp.route('/categories/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            name_en=form.name_en.data,
            description=form.description.data,
            link=form.link.data,
            sort_order=form.sort_order.data,
            is_active=form.is_active.data,
            slug=generate_slug(form.name.data, Category)
        )
        if form.image.data:
            filename = save_file(form.image.data, 'categories')
            if filename:
                category.image = filename
        db.session.add(category)
        db.session.commit()
        flash('تم إنشاء القسم', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/category_form.html', form=form, title='إضافة قسم جديد')


@admin_bp.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        old_image = category.image
        form.populate_obj(category)
        if form.image.data and hasattr(form.image.data, 'filename'):
            if old_image:
                delete_file(old_image, 'categories')
            filename = save_file(form.image.data, 'categories')
            if filename:
                category.image = filename
        else:
            category.image = old_image
        db.session.commit()
        flash('تم تحديث القسم', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/category_form.html', form=form, title='تعديل القسم', category=category)


@admin_bp.route('/categories/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    if category.image:
        delete_file(category.image, 'categories')
    db.session.delete(category)
    db.session.commit()
    flash('تم حذف القسم', 'success')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/home/hero', methods=['GET', 'POST'])
@login_required
@admin_required
def hero_section():
    hero = HeroSection.query.first()
    if not hero:
        hero = HeroSection(title='مرحباً بكم في المعرض الإلكتروني للمدارس')
        db.session.add(hero)
        db.session.commit()

    form = HeroSectionForm(obj=hero)
    if form.validate_on_submit():
        old_bg_image = hero.background_image
        old_bg_video = hero.background_video
        old_demo_video = hero.demo_video
        form.populate_obj(hero)
        if form.background_image.data and hasattr(form.background_image.data, 'filename'):
            if old_bg_image:
                delete_file(old_bg_image, 'home')
            filename = save_file(form.background_image.data, 'home')
            if filename:
                hero.background_image = filename
        else:
            hero.background_image = old_bg_image
        if form.background_video.data and hasattr(form.background_video.data, 'filename'):
            if old_bg_video:
                delete_file(old_bg_video, 'home')
            filename = save_file(form.background_video.data, 'home')
            if filename:
                hero.background_video = filename
        else:
            hero.background_video = old_bg_video
        if form.demo_video.data and hasattr(form.demo_video.data, 'filename'):
            if old_demo_video:
                delete_file(old_demo_video, 'home')
            filename = save_file(form.demo_video.data, 'home')
            if filename:
                hero.demo_video = filename
        else:
            hero.demo_video = old_demo_video
        db.session.commit()
        flash('تم تحديث القسم الرئيسي', 'success')

    return render_template('admin/hero_form.html', form=form, hero=hero)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    role = request.args.get('role', 'all')
    query = User.query
    if role != 'all':
        query = query.filter_by(role=role)
    users = query.order_by(desc(User.created_at)).paginate(page=page, per_page=20)
    return render_template('admin/users.html', users=users, role=role)


@admin_bp.route('/users/toggle/<int:id>', methods=['POST'])
@login_required
@admin_required
def toggle_user(id):
    user = User.query.get_or_404(id)
    if user.is_admin():
        flash('لا يمكن تعطيل حساب الأدمن', 'danger')
        return redirect(url_for('admin.users'))
    user.is_active = not user.is_active
    db.session.commit()
    flash('تم تحديث حالة المستخدم', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.is_admin():
        flash('لا يمكن حذف الأدمن', 'danger')
        return redirect(url_for('admin.users'))
    if user.is_school() and user.school:
        db.session.delete(user.school)
    if user.is_parent() and user.parent:
        db.session.delete(user.parent)
    db.session.delete(user)
    db.session.commit()
    flash('تم حذف المستخدم', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/notifications')
@login_required
@admin_required
def notifications():
    notifs = Notification.query.order_by(desc(Notification.created_at)).all()
    return render_template('admin/notifications.html', notifications=notifs)


@admin_bp.route('/notifications/send', methods=['GET', 'POST'])
@login_required
@admin_required
def send_notification():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        title = request.form.get('title')
        message = request.form.get('message')
        notif_type = request.form.get('type', 'admin_message')

        if user_id == 'all':
            users = User.query.filter_by(is_active=True).all()
            for user in users:
                notif = Notification(
                    user_id=user.id,
                    title=title,
                    message=message,
                    notification_type=notif_type
                )
                db.session.add(notif)
        else:
            notif = Notification(
                user_id=int(user_id),
                title=title,
                message=message,
                notification_type=notif_type
            )
            db.session.add(notif)
        db.session.commit()
        flash('تم إرسال الإشعار', 'success')
        return redirect(url_for('admin.notifications'))

    users = User.query.filter_by(is_active=True).all()
    return render_template('admin/send_notification.html', users=users)


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    setting = Setting.query.first()
    if not setting:
        setting = Setting()
        db.session.add(setting)
        db.session.commit()

    if request.method == 'POST':
        setting.site_name = request.form.get('site_name')
        setting.site_name_en = request.form.get('site_name_en')
        setting.site_description = request.form.get('site_description')
        setting.contact_email = request.form.get('contact_email')
        setting.contact_phone = request.form.get('contact_phone')
        setting.address = request.form.get('address')
        setting.facebook = request.form.get('facebook')
        setting.twitter = request.form.get('twitter')
        setting.instagram = request.form.get('instagram')
        setting.whatsapp = request.form.get('whatsapp')
        setting.primary_color = request.form.get('primary_color', '#6366f1')
        setting.secondary_color = request.form.get('secondary_color', '#ec4899')
        setting.theme = request.form.get('theme', 'light')
        setting.currency = request.form.get('currency', 'EGP')
        setting.bank_transfer_number = request.form.get('bank_transfer_number')
        setting.instapay_phone = request.form.get('instapay_phone')

        if 'logo' in request.files and request.files['logo'].filename:
            if setting.logo:
                delete_file(setting.logo, 'settings')
            filename = save_file(request.files['logo'], 'settings')
            if filename:
                setting.logo = filename

        if 'favicon' in request.files and request.files['favicon'].filename:
            if setting.favicon:
                delete_file(setting.favicon, 'settings')
            filename = save_file(request.files['favicon'], 'settings')
            if filename:
                setting.favicon = filename

        db.session.commit()
        flash('تم حفظ الإعدادات', 'success')
        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html', setting=setting)


# ═══════════════════ HOME CONTENT MANAGEMENT ═══════════════════

@admin_bp.route('/features')
@login_required
@admin_required
def features():
    features = Feature.query.order_by(Feature.sort_order).all()
    return render_template('admin/features.html', features=features)


@admin_bp.route('/features/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_feature():
    form = FeatureForm()
    if form.validate_on_submit():
        feature = Feature(
            icon=form.icon.data, title=form.title.data, title_en=form.title_en.data,
            description=form.description.data, description_en=form.description_en.data,
            sort_order=form.sort_order.data, is_active=form.is_active.data)
        db.session.add(feature)
        db.session.commit()
        flash('تم إضافة الميزة', 'success')
        return redirect(url_for('admin.features'))
    return render_template('admin/feature_form.html', form=form, title='إضافة ميزة جديدة')


@admin_bp.route('/features/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_feature(id):
    feature = Feature.query.get_or_404(id)
    form = FeatureForm(obj=feature)
    if form.validate_on_submit():
        form.populate_obj(feature)
        db.session.commit()
        flash('تم تحديث الميزة', 'success')
        return redirect(url_for('admin.features'))
    return render_template('admin/feature_form.html', form=form, title='تعديل الميزة', feature=feature)


@admin_bp.route('/features/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_feature(id):
    feature = Feature.query.get_or_404(id)
    db.session.delete(feature)
    db.session.commit()
    flash('تم حذف الميزة', 'success')
    return redirect(url_for('admin.features'))


@admin_bp.route('/stats')
@login_required
@admin_required
def stats():
    stats = Stat.query.order_by(Stat.sort_order).all()
    return render_template('admin/stats.html', stats=stats)


@admin_bp.route('/stats/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_stat():
    form = StatForm()
    if form.validate_on_submit():
        stat = Stat(
            icon=form.icon.data, value=form.value.data, label=form.label.data, label_en=form.label_en.data,
            sort_order=form.sort_order.data, is_active=form.is_active.data)
        db.session.add(stat)
        db.session.commit()
        flash('تم إضافة الإحصائية', 'success')
        return redirect(url_for('admin.stats'))
    return render_template('admin/stat_form.html', form=form, title='إضافة إحصائية جديدة')


@admin_bp.route('/stats/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_stat(id):
    stat = Stat.query.get_or_404(id)
    form = StatForm(obj=stat)
    if form.validate_on_submit():
        form.populate_obj(stat)
        db.session.commit()
        flash('تم تحديث الإحصائية', 'success')
        return redirect(url_for('admin.stats'))
    return render_template('admin/stat_form.html', form=form, title='تعديل الإحصائية', stat=stat)


@admin_bp.route('/stats/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_stat(id):
    stat = Stat.query.get_or_404(id)
    db.session.delete(stat)
    db.session.commit()
    flash('تم حذف الإحصائية', 'success')
    return redirect(url_for('admin.stats'))


@admin_bp.route('/gallery')
@login_required
@admin_required
def gallery():
    items = GalleryItem.query.order_by(GalleryItem.sort_order).all()
    return render_template('admin/gallery.html', items=items)


@admin_bp.route('/gallery/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_gallery_item():
    form = GalleryItemForm()
    if form.validate_on_submit():
        item = GalleryItem(
            title=form.title.data, title_en=form.title_en.data,
            tag=form.tag.data, tag_en=form.tag_en.data,
            school_name=form.school_name.data, school_name_en=form.school_name_en.data,
            sort_order=form.sort_order.data, is_active=form.is_active.data)
        if form.image_url.data:
            item.image = form.image_url.data
        elif form.image.data:
            filename = save_file(form.image.data, 'gallery')
            if filename:
                item.image = filename
        db.session.add(item)
        db.session.commit()
        flash('تم إضافة العنصر', 'success')
        return redirect(url_for('admin.gallery'))
    return render_template('admin/gallery_form.html', form=form, title='إضافة عنصر معرض')


@admin_bp.route('/gallery/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_gallery_item(id):
    item = GalleryItem.query.get_or_404(id)
    form = GalleryItemForm(obj=item)
    if form.validate_on_submit():
        old_image = item.image
        form.populate_obj(item)
        if form.image_url.data:
            item.image = form.image_url.data
        elif form.image.data and hasattr(form.image.data, 'filename'):
            if old_image and not old_image.startswith('http'):
                delete_file(old_image, 'gallery')
            filename = save_file(form.image.data, 'gallery')
            if filename:
                item.image = filename
        else:
            item.image = old_image
        db.session.commit()
        flash('تم تحديث العنصر', 'success')
        return redirect(url_for('admin.gallery'))
    return render_template('admin/gallery_form.html', form=form, title='تعديل عنصر المعرض', item=item)


@admin_bp.route('/gallery/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_gallery_item(id):
    item = GalleryItem.query.get_or_404(id)
    if item.image and not item.image.startswith('http'):
        delete_file(item.image, 'gallery')
    db.session.delete(item)
    db.session.commit()
    flash('تم حذف العنصر', 'success')
    return redirect(url_for('admin.gallery'))


@admin_bp.route('/steps')
@login_required
@admin_required
def steps():
    steps = Step.query.order_by(Step.sort_order).all()
    return render_template('admin/steps.html', steps=steps)


@admin_bp.route('/steps/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_step():
    form = StepForm()
    if form.validate_on_submit():
        step = Step(
            icon=form.icon.data, title=form.title.data, title_en=form.title_en.data,
            description=form.description.data, description_en=form.description_en.data,
            tag=form.tag.data, tag_en=form.tag_en.data,
            sort_order=form.sort_order.data, is_active=form.is_active.data)
        db.session.add(step)
        db.session.commit()
        flash('تم إضافة الخطوة', 'success')
        return redirect(url_for('admin.steps'))
    return render_template('admin/step_form.html', form=form, title='إضافة خطوة جديدة')


@admin_bp.route('/steps/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_step(id):
    step = Step.query.get_or_404(id)
    form = StepForm(obj=step)
    if form.validate_on_submit():
        form.populate_obj(step)
        db.session.commit()
        flash('تم تحديث الخطوة', 'success')
        return redirect(url_for('admin.steps'))
    return render_template('admin/step_form.html', form=form, title='تعديل الخطوة', step=step)


@admin_bp.route('/steps/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_step(id):
    step = Step.query.get_or_404(id)
    db.session.delete(step)
    db.session.commit()
    flash('تم حذف الخطوة', 'success')
    return redirect(url_for('admin.steps'))


@admin_bp.route('/testimonials')
@login_required
@admin_required
def testimonials():
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials.html', testimonials=testimonials)


@admin_bp.route('/testimonials/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_testimonial():
    form = TestimonialForm()
    if form.validate_on_submit():
        testimonial = Testimonial(
            text=form.text.data, text_en=form.text_en.data,
            author_name=form.author_name.data, author_name_en=form.author_name_en.data,
            author_role=form.author_role.data, author_role_en=form.author_role_en.data,
            rating=form.rating.data, is_active=form.is_active.data)
        if form.image_url.data:
            testimonial.image = form.image_url.data
        elif form.image.data:
            filename = save_file(form.image.data, 'testimonials')
            if filename:
                testimonial.image = filename
        db.session.add(testimonial)
        db.session.commit()
        flash('تم إضافة التوصية', 'success')
        return redirect(url_for('admin.testimonials'))
    return render_template('admin/testimonial_form.html', form=form, title='إضافة توصية')


@admin_bp.route('/testimonials/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_testimonial(id):
    testimonial = Testimonial.query.get_or_404(id)
    form = TestimonialForm(obj=testimonial)
    if form.validate_on_submit():
        old_image = testimonial.image
        form.populate_obj(testimonial)
        if form.image_url.data:
            testimonial.image = form.image_url.data
        elif form.image.data and hasattr(form.image.data, 'filename'):
            if old_image and not old_image.startswith('http'):
                delete_file(old_image, 'testimonials')
            filename = save_file(form.image.data, 'testimonials')
            if filename:
                testimonial.image = filename
        else:
            testimonial.image = old_image
        db.session.commit()
        flash('تم تحديث التوصية', 'success')
        return redirect(url_for('admin.testimonials'))
    return render_template('admin/testimonial_form.html', form=form, title='تعديل التوصية', testimonial=testimonial)


@admin_bp.route('/testimonials/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_testimonial(id):
    testimonial = Testimonial.query.get_or_404(id)
    if testimonial.image and not testimonial.image.startswith('http'):
        delete_file(testimonial.image, 'testimonials')
    db.session.delete(testimonial)
    db.session.commit()
    flash('تم حذف التوصية', 'success')
    return redirect(url_for('admin.testimonials'))


@admin_bp.route('/faq')
@login_required
@admin_required
def faq():
    faqs = FaqItem.query.order_by(FaqItem.sort_order).all()
    return render_template('admin/faq.html', faqs=faqs)


@admin_bp.route('/faq/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_faq():
    form = FaqItemForm()
    if form.validate_on_submit():
        faq = FaqItem(
            question=form.question.data, question_en=form.question_en.data,
            answer=form.answer.data, answer_en=form.answer_en.data,
            sort_order=form.sort_order.data, is_active=form.is_active.data)
        db.session.add(faq)
        db.session.commit()
        flash('تم إضافة السؤال', 'success')
        return redirect(url_for('admin.faq'))
    return render_template('admin/faq_form.html', form=form, title='إضافة سؤال جديد')


@admin_bp.route('/faq/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_faq(id):
    faq = FaqItem.query.get_or_404(id)
    form = FaqItemForm(obj=faq)
    if form.validate_on_submit():
        form.populate_obj(faq)
        db.session.commit()
        flash('تم تحديث السؤال', 'success')
        return redirect(url_for('admin.faq'))
    return render_template('admin/faq_form.html', form=form, title='تعديل السؤال', faq=faq)


@admin_bp.route('/faq/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_faq(id):
    faq = FaqItem.query.get_or_404(id)
    db.session.delete(faq)
    db.session.commit()
    flash('تم حذف السؤال', 'success')
    return redirect(url_for('admin.faq'))


# ═══════════════════ AI KNOWLEDGE MANAGEMENT ═══════════════════

@admin_bp.route('/ai-knowledge')
@login_required
@admin_required
def ai_knowledge():
    items = AiKnowledge.query.order_by(AiKnowledge.sort_order, AiKnowledge.category).all()
    categories = db.session.query(AiKnowledge.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    return render_template('admin/ai_knowledge.html', items=items, categories=categories)


@admin_bp.route('/ai-knowledge/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_ai_knowledge():
    if request.method == 'POST':
        keywords = request.form.get('keywords', '').strip()
        answer_ar = request.form.get('answer_ar', '').strip()
        answer_en = request.form.get('answer_en', '').strip()
        category = request.form.get('category', 'general').strip()
        sort_order = request.form.get('sort_order', 0, type=int)
        is_active = request.form.get('is_active') == 'on'

        if not keywords or not answer_ar or not answer_en:
            flash('الكلمات المفتاحية والإجابات مطلوبة', 'danger')
            return render_template('admin/ai_knowledge_form.html', title='إضافة معرفة جديدة', item=None)

        item = AiKnowledge(
            keywords=keywords,
            answer_ar=answer_ar,
            answer_en=answer_en,
            category=category,
            sort_order=sort_order,
            is_active=is_active
        )
        db.session.add(item)
        db.session.commit()
        flash('تم إضافة المعرفة', 'success')
        return redirect(url_for('admin.ai_knowledge'))

    return render_template('admin/ai_knowledge_form.html', title='إضافة معرفة جديدة', item=None)


@admin_bp.route('/ai-knowledge/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_ai_knowledge(id):
    item = AiKnowledge.query.get_or_404(id)
    if request.method == 'POST':
        item.keywords = request.form.get('keywords', '').strip()
        item.answer_ar = request.form.get('answer_ar', '').strip()
        item.answer_en = request.form.get('answer_en', '').strip()
        item.category = request.form.get('category', 'general').strip()
        item.sort_order = request.form.get('sort_order', 0, type=int)
        item.is_active = request.form.get('is_active') == 'on'
        db.session.commit()
        flash('تم تحديث المعرفة', 'success')
        return redirect(url_for('admin.ai_knowledge'))

    return render_template('admin/ai_knowledge_form.html', title='تعديل المعرفة', item=item)


@admin_bp.route('/ai-knowledge/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_ai_knowledge(id):
    item = AiKnowledge.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('تم حذف المعرفة', 'success')
    return redirect(url_for('admin.ai_knowledge'))
