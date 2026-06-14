from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User


class LoginForm(FlaskForm):
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    password = PasswordField('كلمة المرور', validators=[DataRequired()])
    remember = BooleanField('تذكرني')
    submit = SubmitField('تسجيل الدخول')


class SchoolRegisterForm(FlaskForm):
    school_name = StringField('اسم المدرسة', validators=[DataRequired(), Length(min=2, max=200)])
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    phone = StringField('رقم الجوال', validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField('كلمة المرور', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')])
    plan_id = SelectField('الباقة', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Register School')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('البريد الإلكتروني مسجل بالفعل')


class ParentRegisterForm(FlaskForm):
    full_name = StringField('الاسم الكامل', validators=[DataRequired(), Length(min=2, max=200)])
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    phone = StringField('رقم الجوال', validators=[Length(max=20)])
    password = PasswordField('كلمة المرور', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')])
    children_count = IntegerField('عدد الأبناء', default=0)
    submit = SubmitField('تسجيل حساب')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('البريد الإلكتروني مسجل بالفعل')
