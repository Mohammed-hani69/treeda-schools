from flask import Blueprint, render_template, request, abort, current_app
from flask_login import login_required, current_user
from app import db
from app.models.school import School, SchoolMedia, SchoolVisitLog
from app.models.parent import Parent
from app.utils.decorators import parent_required, login_or_redirect
from sqlalchemy import or_, desc

parent_bp = Blueprint('parent', __name__)


@parent_bp.route('/dashboard')
@login_required
@parent_required
def dashboard():
    parent = Parent.query.filter_by(user_id=current_user.id).first()
    recent_schools = School.query.filter_by(is_approved=True, is_active=True)\
        .order_by(desc(School.created_at)).limit(6).all()
    return render_template('parent/dashboard.html',
                         parent=parent, recent_schools=recent_schools)


@parent_bp.route('/schools')
@login_required
@parent_required
def schools():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    city = request.args.get('city', '')
    school_type = request.args.get('type', '')
    gender = request.args.get('gender', '')
    per_page = current_app.config.get('SCHOOLS_PER_PAGE', 20)

    query = School.query.filter_by(is_approved=True, is_active=True)

    if search:
        query = query.filter(
            or_(School.name.ilike(f'%{search}%'),
                School.about.ilike(f'%{search}%'),
                School.city.ilike(f'%{search}%'))
        )
    if city:
        query = query.filter(School.city.ilike(f'%{city}%'))
    if school_type:
        query = query.filter_by(school_type=school_type)
    if gender:
        query = query.filter_by(gender=gender)

    schools = query.order_by(desc(School.is_featured), desc(School.created_at))\
        .paginate(page=page, per_page=per_page)
    cities = db.session.query(School.city).filter(
        School.city.isnot(None), School.city != '',
        School.is_approved == True, School.is_active == True
    ).distinct().all()
    cities = [c[0] for c in cities if c[0]]

    return render_template('parent/schools.html',
                         schools=schools, cities=cities,
                         search=search, city=city,
                         school_type=school_type, gender=gender)


@parent_bp.route('/school/<slug>')
@login_required
@login_or_redirect
def school_detail(slug):
    school = School.query.filter_by(slug=slug, is_active=True).first_or_404()
    school.views = (school.views or 0) + 1
    SchoolVisitLog.record_visit(school.id)
    db.session.commit()

    images = school.approved_media('image').order_by(desc(SchoolMedia.created_at)).all()
    videos = school.approved_media('video').order_by(desc(SchoolMedia.created_at)).all()

    return render_template('parent/school_detail.html',
                         school=school, images=images, videos=videos)
