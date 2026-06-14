from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.models.school import School
from app.models.parent import Parent
from app.models.plan import Plan
from app.models.notification import Notification
from app.forms.auth_forms import LoginForm, SchoolRegisterForm, ParentRegisterForm
from app.utils.helpers import generate_slug

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        if current_user.is_school():
            return redirect(url_for('school.dashboard'))
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('تم تعطيل حسابك. يرجى التواصل مع الإدارة.', 'danger')
                return render_template('auth/login.html', form=form)
            login_user(user, remember=form.remember.data)
            user.last_login = __import__('datetime').datetime.utcnow()
            db.session.commit()
            flash('تم تسجيل الدخول بنجاح', 'success')
            next_page = request.args.get('next')

            if user.is_admin():
                return redirect(next_page or url_for('admin.dashboard'))
            if user.is_school():
                return redirect(next_page or url_for('school.dashboard'))
            return redirect(next_page or url_for('main.index'))
        flash('بريد إلكتروني أو كلمة مرور غير صحيحة', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register/school', methods=['GET', 'POST'])
def register_school():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = SchoolRegisterForm()
    form.plan_id.choices = [(p.id, f"{p.name} - {p.price} جنيه") for p in Plan.query.filter_by(is_active=True).order_by(Plan.sort_order).all()]

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('البريد الإلكتروني مسجل بالفعل', 'danger')
            return render_template('auth/register_school.html', form=form)

        user = User(
            username=f"school_{form.email.data.split('@')[0]}",
            email=form.email.data,
            role='school',
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        slug = generate_slug(form.school_name.data, School)
        school = School(
            user_id=user.id,
            name=form.school_name.data,
            slug=slug,
            phone=form.phone.data,
            email=form.email.data
        )
        db.session.add(school)

        plan = Plan.query.get(form.plan_id.data)
        if plan:
            from datetime import datetime, timedelta
            from app.models.plan import Subscription
            subscription = Subscription(
                school_id=school.id,
                plan_id=plan.id,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=plan.duration_days),
                price_paid=plan.price,
                status='pending'
            )
            db.session.add(subscription)

        db.session.commit()

        flash('تم تسجيل المدرسة بنجاح. سيتم مراجعة طلبك من قبل الإدارة.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register_school.html', form=form)


@auth_bp.route('/register/parent', methods=['GET', 'POST'])
def register_parent():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ParentRegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('البريد الإلكتروني مسجل بالفعل', 'danger')
            return render_template('auth/register_parent.html', form=form)

        user = User(
            username=f"parent_{form.email.data.split('@')[0]}",
            email=form.email.data,
            role='parent',
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        parent = Parent(
            user_id=user.id,
            full_name=form.full_name.data,
            phone=form.phone.data,
            children_count=form.children_count.data
        )
        db.session.add(parent)
        db.session.commit()

        flash('تم تسجيل الحساب بنجاح. يمكنك الآن تسجيل الدخول.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register_parent.html', form=form)


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = LoginForm()  # dummy, just for CSRF
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = User.query.filter_by(email=email).first()
        if user:
            flash('تم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني.', 'success')
        else:
            flash('البريد الإلكتروني غير مسجل في المنصة.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('main.index'))
