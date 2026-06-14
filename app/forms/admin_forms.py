from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, IntegerField, FloatField, SelectField, URLField, DateTimeField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, Email, URL


class PlanForm(FlaskForm):
    name = StringField('اسم الباقة', validators=[DataRequired(), Length(max=100)])
    name_en = StringField('اسم الباقة (إنجليزي)', validators=[Optional(), Length(max=100)])
    description = TextAreaField('وصف الباقة')
    price = FloatField('السعر', validators=[DataRequired()])
    currency = StringField('العملة', default='EGP')
    duration_days = IntegerField('مدة الاشتراك (أيام)', validators=[DataRequired()])
    max_images = IntegerField('الحد الأقصى للصور', default=10)
    max_videos = IntegerField('الحد الأقصى للفيديوهات', default=5)
    storage_mb = IntegerField('مساحة التخزين (ميجابايت)', default=100)
    max_employees = IntegerField('عدد الموظفين المسموح', default=5)
    image = FileField('صورة الباقة', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    is_featured = BooleanField('ظهور مميز')
    color = StringField('لون الباقة', default='#6366f1')
    sort_order = IntegerField('ترتيب الظهور', default=0)
    is_active = BooleanField('مفعلة', default=True)
    features = TextAreaField('المميزات (كل ميزة في سطر)')
    submit = SubmitField('حفظ')


class CategoryForm(FlaskForm):
    name = StringField('اسم القسم', validators=[DataRequired(), Length(max=200)])
    name_en = StringField('اسم القسم (إنجليزي)', validators=[Optional(), Length(max=200)])
    description = TextAreaField('الوصف')
    image = FileField('الصورة', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    link = StringField('الرابط')
    sort_order = IntegerField('الترتيب', default=0)
    is_active = BooleanField('ظاهر', default=True)
    submit = SubmitField('حفظ')


class HomeSectionForm(FlaskForm):
    section_type = SelectField('نوع القسم', choices=[
        ('text', 'نص فقط'),
        ('image_text', 'صورة + نص'),
        ('video_text', 'فيديو + نص'),
        ('image_slider', 'سلايدر صور'),
        ('video_slider', 'سلايدر فيديوهات'),
        ('cards', 'بطاقات'),
        ('stats', 'إحصائيات'),
        ('faq', 'أسئلة شائعة'),
        ('gallery', 'معرض صور'),
        ('video_gallery', 'معرض فيديوهات'),
        ('image_links', 'صور تحتوي روابط'),
        ('cta', 'زر CTA'),
        ('builtin_hero', 'القسم الرئيسي (Hero)'),
        ('builtin_stats', 'شريط الإحصائيات'),
        ('builtin_features', 'الميزات (لماذا نحن)'),
        ('builtin_categories', 'أقسام المدارس'),
        ('builtin_featured_schools', 'المدارس المميزة'),
        ('builtin_gallery', 'معرض الصور'),
        ('builtin_steps', 'خطوات العمل'),
        ('builtin_pricing', 'الباقات والأسعار'),
        ('builtin_testimonials', 'التوصيات'),
        ('builtin_faq', 'الأسئلة الشائعة'),
        ('builtin_cta', 'دعوة للإجراء (CTA)'),
    ])
    title = StringField('العنوان', validators=[Optional(), Length(max=300)])
    subtitle = StringField('العنوان الفرعي', validators=[Optional(), Length(max=500)])
    description = TextAreaField('الوصف')
    background_color = StringField('لون الخلفية')
    background_image = FileField('صورة الخلفية', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    padding_top = IntegerField('الحشوة العلوية', default=60)
    padding_bottom = IntegerField('الحشوة السفلية', default=60)
    text_color = StringField('لون النص')
    sort_order = IntegerField('الترتيب', default=0)
    is_active = BooleanField('ظاهر', default=True)
    submit = SubmitField('حفظ')


class HeroSectionForm(FlaskForm):
    title = StringField('العنوان الرئيسي', validators=[DataRequired(), Length(max=300)])
    subtitle = StringField('العنوان الفرعي', validators=[Optional(), Length(max=500)])
    description = TextAreaField('الوصف')
    background_type = SelectField('نوع الخلفية', choices=[('image', 'صورة'), ('video', 'فيديو'), ('color', 'لون')])
    background_image = FileField('صورة الخلفية', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    background_video = FileField('فيديو الخلفية', validators=[FileAllowed(['mp4', 'mov', 'avi', 'webm'])])
    background_color = StringField('لون الخلفية', default='#1e1b4b')
    demo_video = FileField('فيديو العرض التوضيحي', validators=[FileAllowed(['mp4', 'mov', 'avi', 'webm'])])
    button1_text = StringField('نص الزر الأول', validators=[Optional(), Length(max=100)])
    button1_link = StringField('رابط الزر الأول')
    button2_text = StringField('نص الزر الثاني', validators=[Optional(), Length(max=100)])
    button2_link = StringField('رابط الزر الثاني')
    overlay_opacity = FloatField('شفافية الطبقة', default=0.5)
    is_active = BooleanField('نشط', default=True)
    submit = SubmitField('حفظ')


class FeatureForm(FlaskForm):
    icon = StringField('الأيقونة (اسم Bootstrap icon)', default='stars')
    title = StringField('العنوان', validators=[DataRequired(), Length(max=200)])
    title_en = StringField('العنوان (إنجليزي)', validators=[Optional(), Length(max=200)])
    description = TextAreaField('الوصف')
    description_en = TextAreaField('الوصف (إنجليزي)')
    sort_order = IntegerField('الترتيب', default=0)
    is_active = BooleanField('ظاهر', default=True)
    submit = SubmitField('حفظ')


class StatForm(FlaskForm):
    icon = StringField('الأيقونة (اسم Bootstrap icon)', default='mortarboard')
    value = StringField('القيمة الرقمية (مثال: 250+)', validators=[DataRequired(), Length(max=50)])
    label = StringField('التسمية', validators=[DataRequired(), Length(max=200)])
    label_en = StringField('التسمية (إنجليزي)', validators=[Optional(), Length(max=200)])
    sort_order = IntegerField('الترتيب', default=0)
    is_active = BooleanField('ظاهر', default=True)
    submit = SubmitField('حفظ')


class GalleryItemForm(FlaskForm):
    image = FileField('الصورة', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    image_url = StringField('رابط الصورة (خارجي)', validators=[Optional()])
    title = StringField('العنوان', validators=[DataRequired(), Length(max=200)])
    title_en = StringField('العنوان (إنجليزي)', validators=[Optional(), Length(max=200)])
    tag = StringField('الوسم', validators=[Optional(), Length(max=100)])
    tag_en = StringField('الوسم (إنجليزي)', validators=[Optional(), Length(max=100)])
    school_name = StringField('اسم المدرسة', validators=[Optional(), Length(max=200)])
    school_name_en = StringField('اسم المدرسة (إنجليزي)', validators=[Optional(), Length(max=200)])
    sort_order = IntegerField('الترتيب', default=0)
    is_active = BooleanField('ظاهر', default=True)
    submit = SubmitField('حفظ')


class StepForm(FlaskForm):
    icon = StringField('الأيقونة (اسم Bootstrap icon)', default='people')
    title = StringField('العنوان', validators=[DataRequired(), Length(max=200)])
    title_en = StringField('العنوان (إنجليزي)', validators=[Optional(), Length(max=200)])
    description = TextAreaField('الوصف')
    description_en = TextAreaField('الوصف (إنجليزي)')
    tag = StringField('الوسم', validators=[Optional(), Length(max=100)])
    tag_en = StringField('الوسم (إنجليزي)', validators=[Optional(), Length(max=100)])
    sort_order = IntegerField('الترتيب', default=0)
    is_active = BooleanField('ظاهر', default=True)
    submit = SubmitField('حفظ')


class TestimonialForm(FlaskForm):
    image = FileField('الصورة', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    image_url = StringField('رابط الصورة (خارجي)', validators=[Optional()])
    text = TextAreaField('النص', validators=[DataRequired()])
    text_en = TextAreaField('النص (إنجليزي)')
    author_name = StringField('اسم الكاتب', validators=[DataRequired(), Length(max=200)])
    author_name_en = StringField('اسم الكاتب (إنجليزي)', validators=[Optional(), Length(max=200)])
    author_role = StringField('الدور', validators=[Optional(), Length(max=200)])
    author_role_en = StringField('الدور (إنجليزي)', validators=[Optional(), Length(max=200)])
    rating = IntegerField('التقييم (من 5)', default=5)
    is_active = BooleanField('ظاهر', default=True)
    submit = SubmitField('حفظ')


class FaqItemForm(FlaskForm):
    question = StringField('السؤال', validators=[DataRequired(), Length(max=300)])
    question_en = StringField('السؤال (إنجليزي)', validators=[Optional(), Length(max=300)])
    answer = TextAreaField('الإجابة', validators=[DataRequired()])
    answer_en = TextAreaField('الإجابة (إنجليزي)')
    sort_order = IntegerField('الترتيب', default=0)
    is_active = BooleanField('ظاهر', default=True)
    submit = SubmitField('حفظ')


class SchoolEditForm(FlaskForm):
    name = StringField('اسم المدرسة', validators=[DataRequired(), Length(max=200)])
    about = TextAreaField('نبذة عن المدرسة')
    address = StringField('العنوان', validators=[Optional(), Length(max=300)])
    city = StringField('المدينة', validators=[Optional(), Length(max=100)])
    district = StringField('الحي', validators=[Optional(), Length(max=100)])
    phone = StringField('رقم الجوال', validators=[Optional(), Length(max=20)])
    phone2 = StringField('رقم جوال آخر', validators=[Optional(), Length(max=20)])
    email = StringField('البريد الإلكتروني', validators=[Optional(), Email()])
    website = StringField('الموقع الإلكتروني', validators=[Optional(), URL()])
    school_type = SelectField('نوع المدرسة', choices=[
        ('', 'اختر النوع'),
        ('government', 'حكومية'),
        ('private', 'أهلية'),
        ('international', 'دولية'),
        ('quran', 'تحفيظ قرآن'),
    ])
    gender = SelectField('نوع الطلاب', choices=[
        ('', 'اختر النوع'),
        ('male', 'بنين'),
        ('female', 'بنات'),
        ('both', 'مشترك'),
    ])
    founded_year = IntegerField('سنة التأسيس', validators=[Optional()])
    facebook = StringField('فيسبوك', validators=[Optional(), URL()])
    twitter = StringField('تويتر', validators=[Optional(), URL()])
    instagram = StringField('انستغرام', validators=[Optional(), URL()])
    youtube = StringField('يوتيوب', validators=[Optional(), URL()])
    whatsapp = StringField('واتساب', validators=[Optional(), Length(max=20)])
    telegram = StringField('تيليغرام', validators=[Optional(), URL()])
    map_lat = FloatField('خط العرض', validators=[Optional()])
    map_lng = FloatField('خط الطول', validators=[Optional()])
    submit = SubmitField('حفظ')


class AdminSchoolCreateForm(FlaskForm):
    name = StringField('اسم المدرسة', validators=[DataRequired(), Length(max=200)])
    about = TextAreaField('نبذة عن المدرسة')
    address = StringField('العنوان', validators=[Optional(), Length(max=300)])
    city = StringField('المدينة', validators=[Optional(), Length(max=100)])
    district = StringField('الحي', validators=[Optional(), Length(max=100)])
    phone = StringField('رقم الجوال', validators=[Optional(), Length(max=20)])
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    website = StringField('الموقع الإلكتروني', validators=[Optional(), URL()])
    category_id = SelectField('القسم', coerce=int, choices=[])
    gender = SelectField('نوع الطلاب', choices=[
        ('', 'اختر النوع'),
        ('male', 'بنين'),
        ('female', 'بنات'),
        ('both', 'مشترك'),
    ])
    logo = FileField('اللوجو', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    cover = FileField('صورة الغلاف', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    image = FileField('الصورة الخارجية', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    username = StringField('اسم المستخدم', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('كلمة المرور', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('حفظ')


class SubscriptionForm(FlaskForm):
    school_id = SelectField('المدرسة', coerce=int, validators=[DataRequired()])
    plan_id = SelectField('الباقة', coerce=int, validators=[DataRequired()])
    start_date = DateTimeField('تاريخ البداية', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    end_date = DateTimeField('تاريخ النهاية', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    status = SelectField('الحالة', choices=[('active', 'نشط'), ('inactive', 'غير نشط'), ('expired', 'منتهي')], default='active')
    auto_renew = BooleanField('تجديد تلقائي')
    price_paid = FloatField('المبلغ المدفوع', validators=[Optional()])
    submit = SubmitField('حفظ')
