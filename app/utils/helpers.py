import os
import uuid
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask import current_app, flash, redirect, url_for
from PIL import Image as PILImage


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})


def is_image(filename):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return ext in {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def is_video(filename):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return ext in {'mp4', 'mov', 'avi', 'webm'}


def save_file(file, subfolder='media'):
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', subfolder)
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)

        if is_image(filename):
            try:
                img = PILImage.open(filepath)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                img.thumbnail((1920, 1080), PILImage.LANCZOS)
                img.save(filepath, quality=85, optimize=True)
            except Exception:
                pass

        return filename
    return None


def delete_file(filename, subfolder='media'):
    if not filename:
        return
    filepath = os.path.join(current_app.root_path, 'static', 'uploads', subfolder, filename)
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass


def format_date(date, fmt='%Y-%m-%d'):
    if date:
        return date.strftime(fmt)
    return ''


def time_ago(date):
    if not date:
        return ''
    now = datetime.utcnow()
    diff = now - date
    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60

    if days > 365:
        return f'منذ {days // 365} سنة'
    if days > 30:
        return f'منذ {days // 30} شهر'
    if days > 7:
        return f'منذ {days // 7} أسبوع'
    if days > 0:
        return f'منذ {days} يوم'
    if hours > 0:
        return f'منذ {hours} ساعة'
    if minutes > 0:
        return f'منذ {minutes} دقيقة'
    return 'الآن'


def slugify(text):
    import re
    text = text.strip().lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:200]


def generate_slug(text, model):
    slug = slugify(text)
    original_slug = slug
    counter = 1
    while model.query.filter_by(slug=slug).first():
        slug = f"{original_slug}-{counter}"
        counter += 1
    return slug


def school_permissions(school):
    """Return permissions dict for a school based on its active subscription."""
    from app.models.plan import Subscription
    from app.models.school import SchoolMedia

    sub = Subscription.query.filter_by(school_id=school.id).first()
    plan = sub.plan if sub else None

    images_used = school.media_count_by_type('image')
    videos_used = school.media_count_by_type('video')
    storage_used = school.storage_used_mb()

    activities_count = school.activities.count()
    services_count = school.services.count()
    grades_count = school.grades.count()

    remaining_images = max(0, (plan.max_images if plan else 0) - images_used)
    remaining_videos = max(0, (plan.max_videos if plan else 0) - videos_used)
    remaining_storage = max(0, (plan.storage_mb if plan else 0) - storage_used)

    return {
        'has_subscription': sub is not None,
        'has_plan': plan is not None,
        'subscription': sub,
        'plan': plan,
        'is_expired': sub.is_expired if sub else True,
        'images_used': images_used,
        'images_max': plan.max_images if plan else 0,
        'videos_used': videos_used,
        'videos_max': plan.max_videos if plan else 0,
        'storage_used': round(storage_used, 1),
        'storage_max': plan.storage_mb if plan else 0,
        'employees_max': plan.max_employees if plan else 0,
        'activities_count': activities_count,
        'services_count': services_count,
        'grades_count': grades_count,
        'remaining_images': remaining_images,
        'remaining_videos': remaining_videos,
        'remaining_storage': round(remaining_storage, 1),
        'can_upload': sub is not None and not sub.is_expired,
    }


def check_upload_permission(school):
    """Check if school can upload based on subscription and limits. Returns error message or None."""
    from app.models.plan import Subscription

    sub = Subscription.query.filter_by(school_id=school.id).first()
    if not sub:
        return 'لا يوجد اشتراك نشط. يرجى التواصل مع الإدارة.'
    if sub.is_expired:
        return 'انتهت صلاحية الاشتراك. يرجى تجديد الاشتراك.'
    return None


def check_image_limit(school):
    """Check if school reached max images. Returns error message or None."""
    from app.models.plan import Subscription

    sub = Subscription.query.filter_by(school_id=school.id).first()
    if sub and sub.plan:
        used = school.media_count_by_type('image')
        if used >= sub.plan.max_images:
            return f'لقد وصلت للحد المسموح من الصور ({sub.plan.max_images}).'
    return None


def check_video_limit(school):
    """Check if school reached max videos. Returns error message or None."""
    from app.models.plan import Subscription

    sub = Subscription.query.filter_by(school_id=school.id).first()
    if sub and sub.plan:
        used = school.media_count_by_type('video')
        if used >= sub.plan.max_videos:
            return f'لقد وصلت للحد المسموح من الفيديوهات ({sub.plan.max_videos}).'
    return None


def check_storage_limit(school, file_size):
    """Check if adding file would exceed storage. Returns error message or None."""
    from app.models.plan import Subscription

    sub = Subscription.query.filter_by(school_id=school.id).first()
    if sub and sub.plan:
        used_mb = school.storage_used_mb()
        file_mb = file_size / (1024 * 1024)
        if used_mb + file_mb > sub.plan.storage_mb:
            return f'مساحة التخزين غير كافية. المستخدم: {used_mb:.1f}MB / المسموح: {sub.plan.storage_mb}MB.'
    return None
