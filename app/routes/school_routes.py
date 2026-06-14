from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.school import School, SchoolMedia, SchoolActivity, SchoolService, SchoolGrade, SchoolVisitLog
from app.models.plan import Subscription
from app.models.notification import Notification
from app.utils.decorators import school_required
from app.utils.helpers import save_file, delete_file, allowed_file, check_upload_permission, check_image_limit, check_video_limit, check_storage_limit, school_permissions
from app.forms.admin_forms import SchoolEditForm
from werkzeug.utils import secure_filename
import os

school_bp = Blueprint('school', __name__)


@school_bp.context_processor
def inject_school_data():
    if current_user.is_authenticated and current_user.is_school():
        return {
            'unread_count': Notification.query.filter_by(
                user_id=current_user.id, is_read=False
            ).count()
        }
    return {}


@school_bp.before_request
def check_school():
    if current_user.is_authenticated and current_user.is_school():
        school = School.query.filter_by(user_id=current_user.id).first()
        if school and not school.is_approved:
            if request.endpoint not in ['school.dashboard', 'auth.logout']:
                flash('حسابك قيد المراجعة من قبل الإدارة', 'warning')
                return redirect(url_for('school.dashboard'))
        if school and not school.is_approved and request.endpoint == 'school.dashboard':
            pass  # allow dashboard access with pending notice


@school_bp.route('/dashboard')
@login_required
@school_required
def dashboard():
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    subscription = Subscription.query.filter_by(school_id=school.id).first()
    counts = school.get_counts()
    stats = {
        'images': counts['image'],
        'videos': counts['video'],
        'pending': counts['pending'],
        'activities': school.activities.count(),
    }
    recent_media = school.media.order_by(SchoolMedia.created_at.desc()).limit(5).all()
    perms = school_permissions(school)
    return render_template('school/dashboard.html',
                         school=school, subscription=subscription,
                         stats=stats, recent_media=recent_media, perms=perms)


@school_bp.route('/analytics')
@login_required
@school_required
def analytics():
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    from datetime import date, timedelta

    # Last 30 days visit data
    today = date.today()
    thirty_days = [today - timedelta(days=i) for i in range(29, -1, -1)]
    logs = SchoolVisitLog.query.filter(
        SchoolVisitLog.school_id == school.id,
        SchoolVisitLog.date >= thirty_days[0]
    ).order_by(SchoolVisitLog.date).all()

    log_map = {l.date: l.visits for l in logs}
    daily_data = [{'date': d.isoformat(), 'visits': log_map.get(d, 0)} for d in thirty_days]
    total_30 = sum(d['visits'] for d in daily_data)

    # Media counts
    counts = school.get_counts()

    return render_template('school/analytics.html',
                         school=school,
                         total_views=school.views or 0,
                         total_30=total_30,
                         daily_data=daily_data,
                         stats=counts)


@school_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@school_required
def profile():
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    form = SchoolEditForm(obj=school)

    if form.validate_on_submit():
        form.populate_obj(school)
        db.session.commit()
        flash('تم حفظ التعديلات بنجاح', 'success')
        return redirect(url_for('school.profile'))

    return render_template('school/profile.html', form=form, school=school)


@school_bp.route('/media')
@login_required
@school_required
def media():
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    media_type = request.args.get('type', 'all')
    status_filter = request.args.get('status', 'all')

    query = SchoolMedia.query.filter_by(school_id=school.id)
    if media_type != 'all':
        query = query.filter_by(media_type=media_type)
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    media_list = query.order_by(SchoolMedia.created_at.desc()).all()

    perms = school_permissions(school)
    return render_template('school/media.html',
                         school=school, media=media_list, perms=perms)


@school_bp.route('/media/upload', methods=['POST'])
@login_required
@school_required
def upload_media():
    school = School.query.filter_by(user_id=current_user.id).first_or_404()

    err = check_upload_permission(school)
    if err:
        flash(err, 'danger')
        return redirect(url_for('school.media'))

    if 'file' not in request.files:
        flash('لم يتم تحديد ملف', 'danger')
        return redirect(url_for('school.media'))

    file = request.files['file']
    if file.filename == '':
        flash('لم يتم تحديد ملف', 'danger')
        return redirect(url_for('school.media'))

    if not allowed_file(file.filename):
        flash('نوع الملف غير مدعوم', 'danger')
        return redirect(url_for('school.media'))

    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    media_type = 'image' if ext in {'png', 'jpg', 'jpeg', 'gif', 'webp'} else 'video'

    if media_type == 'image':
        err = check_image_limit(school)
        if err:
            flash(err, 'danger')
            return redirect(url_for('school.media'))
    else:
        err = check_video_limit(school)
        if err:
            flash(err, 'danger')
            return redirect(url_for('school.media'))

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    err = check_storage_limit(school, file_size)
    if err:
        flash(err, 'danger')
        return redirect(url_for('school.media'))

    filename = save_file(file, 'media')
    if filename:
        media_item = SchoolMedia(
            school_id=school.id,
            media_type=media_type,
            filename=filename,
            original_name=file.filename,
            status='pending',
            file_size=os.path.getsize(os.path.join(current_app.root_path, 'static', 'uploads', 'media', filename))
        )
        db.session.add(media_item)
        db.session.commit()
        flash('تم رفع الملف بنجاح وسيتم مراجعته', 'success')
    else:
        flash('حدث خطأ أثناء رفع الملف', 'danger')

    return redirect(url_for('school.media'))


@school_bp.route('/media/delete/<int:id>', methods=['POST'])
@login_required
@school_required
def delete_media(id):
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    media_item = SchoolMedia.query.filter_by(id=id, school_id=school.id).first_or_404()
    delete_file(media_item.filename, 'media')
    db.session.delete(media_item)
    db.session.commit()
    flash('تم حذف الملف', 'success')
    return redirect(url_for('school.media'))


@school_bp.route('/activities')
@login_required
@school_required
def activities():
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    activities_list = school.activities.order_by(SchoolActivity.created_at.desc()).all()
    return render_template('school/activities.html', school=school, activities=activities_list)


@school_bp.route('/activities/add', methods=['POST'])
@login_required
@school_required
def add_activity():
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    title = request.form.get('title')
    description = request.form.get('description')
    if title:
        activity = SchoolActivity(school_id=school.id, title=title, description=description)
        db.session.add(activity)
        db.session.commit()
        flash('تم إضافة النشاط', 'success')
    return redirect(url_for('school.activities'))


@school_bp.route('/activities/delete/<int:id>', methods=['POST'])
@login_required
@school_required
def delete_activity(id):
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    activity = SchoolActivity.query.filter_by(id=id, school_id=school.id).first_or_404()
    db.session.delete(activity)
    db.session.commit()
    flash('تم حذف النشاط', 'success')
    return redirect(url_for('school.activities'))


@school_bp.route('/services')
@login_required
@school_required
def services():
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    services_list = school.services.order_by(SchoolService.created_at.desc()).all()
    return render_template('school/services.html', school=school, services=services_list)


@school_bp.route('/services/add', methods=['POST'])
@login_required
@school_required
def add_service():
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    title = request.form.get('title')
    description = request.form.get('description')
    if title:
        service = SchoolService(school_id=school.id, title=title, description=description)
        db.session.add(service)
        db.session.commit()
        flash('تم إضافة الخدمة', 'success')
    return redirect(url_for('school.services'))


@school_bp.route('/services/delete/<int:id>', methods=['POST'])
@login_required
@school_required
def delete_service(id):
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    service = SchoolService.query.filter_by(id=id, school_id=school.id).first_or_404()
    db.session.delete(service)
    db.session.commit()
    flash('تم حذف الخدمة', 'success')
    return redirect(url_for('school.services'))


@school_bp.route('/grades')
@login_required
@school_required
def grades():
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    grades_list = school.grades.order_by(SchoolGrade.name).all()
    return render_template('school/grades.html', school=school, grades=grades_list)


@school_bp.route('/grades/add', methods=['POST'])
@login_required
@school_required
def add_grade():
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    name = request.form.get('name')
    if name:
        grade = SchoolGrade(school_id=school.id, name=name)
        db.session.add(grade)
        db.session.commit()
        flash('تم إضافة المرحلة', 'success')
    return redirect(url_for('school.grades'))


@school_bp.route('/grades/delete/<int:id>', methods=['POST'])
@login_required
@school_required
def delete_grade(id):
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    grade = SchoolGrade.query.filter_by(id=id, school_id=school.id).first_or_404()
    db.session.delete(grade)
    db.session.commit()
    flash('تم حذف المرحلة', 'success')
    return redirect(url_for('school.grades'))


@school_bp.route('/logo/upload', methods=['POST'])
@login_required
@school_required
def upload_logo():
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    if 'logo' in request.files:
        file = request.files['logo']
        if file and allowed_file(file.filename):
            if school.logo:
                delete_file(school.logo, 'schools')
            filename = save_file(file, 'schools')
            if filename:
                school.logo = filename
                db.session.commit()
                flash('تم رفع الشعار بنجاح', 'success')
    return redirect(url_for('school.profile'))


@school_bp.route('/cover/upload', methods=['POST'])
@login_required
@school_required
def upload_cover():
    school = School.query.filter_by(user_id=current_user.id).first_or_404()
    if 'cover' in request.files:
        file = request.files['cover']
        if file and allowed_file(file.filename):
            if school.cover:
                delete_file(school.cover, 'schools')
            filename = save_file(file, 'schools')
            if filename:
                school.cover = filename
                db.session.commit()
                flash('تم رفع الغلاف بنجاح', 'success')
    return redirect(url_for('school.profile'))


@school_bp.route('/notifications')
@login_required
@school_required
def notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id)\
        .order_by(Notification.created_at.desc()).all()
    return render_template('school/notifications.html', notifications=notifs)


@school_bp.route('/notifications/read/<int:id>')
@login_required
@school_required
def read_notification(id):
    notif = Notification.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    notif.is_read = True
    db.session.commit()
    return redirect(notif.link or url_for('school.dashboard'))


@school_bp.route('/notifications/read-all', methods=['POST'])
@login_required
@school_required
def read_all_notifications():
    Notification.query.filter_by(user_id=current_user.id, is_read=False)\
        .update({Notification.is_read: True})
    db.session.commit()
    flash('تم تحديد الكل كمقروء', 'success')
    return redirect(url_for('school.notifications'))
