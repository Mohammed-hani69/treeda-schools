from datetime import datetime
from app import db


class HeroSection(db.Model):
    __tablename__ = 'hero_sections'

    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=True)
    background_type = db.Column(db.String(10), default='image')
    background_image = db.Column(db.String(255))
    background_video = db.Column(db.String(255))
    background_color = db.Column(db.String(20), default='#1e1b4b')
    demo_video = db.Column(db.String(255))
    title = db.Column(db.String(300), nullable=False)
    title_ar = db.Column(db.String(300))
    subtitle = db.Column(db.String(500))
    description = db.Column(db.Text)
    button1_text = db.Column(db.String(100))
    button1_link = db.Column(db.String(255))
    button1_style = db.Column(db.String(50), default='primary')
    button2_text = db.Column(db.String(100))
    button2_link = db.Column(db.String(255))
    button2_style = db.Column(db.String(50), default='outline')
    overlay_opacity = db.Column(db.Float, default=0.5)
    text_color = db.Column(db.String(20), default='#ffffff')
    animation_style = db.Column(db.String(50), default='fade-up')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class HomeSection(db.Model):
    __tablename__ = 'home_sections'

    id = db.Column(db.Integer, primary_key=True)
    section_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(300))
    title_ar = db.Column(db.String(300))
    subtitle = db.Column(db.String(500))
    description = db.Column(db.Text)
    content = db.Column(db.JSON)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    background_color = db.Column(db.String(20))
    background_image = db.Column(db.String(255))
    padding_top = db.Column(db.Integer, default=60)
    padding_bottom = db.Column(db.Integer, default=60)
    text_color = db.Column(db.String(20))
    animation_style = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    SECTION_TYPES = {
        'text': 'نص فقط',
        'image_text': 'صورة + نص',
        'video_text': 'فيديو + نص',
        'image_slider': 'سلايدر صور',
        'video_slider': 'سلايدر فيديوهات',
        'cards': 'بطاقات',
        'stats': 'إحصائيات',
        'faq': 'أسئلة شائعة',
        'gallery': 'معرض صور',
        'video_gallery': 'معرض فيديوهات',
        'image_links': 'صور تحتوي روابط',
        'cta': 'زر CTA',

        'builtin_hero': 'القسم الرئيسي (Hero)',
        'builtin_stats': 'شريط الإحصائيات',
        'builtin_features': 'الميزات (لماذا نحن)',
        'builtin_categories': 'أقسام المدارس',
        'builtin_featured_schools': 'المدارس المميزة',
        'builtin_gallery': 'معرض الصور',
        'builtin_steps': 'خطوات العمل',
        'builtin_pricing': 'الباقات والأسعار',
        'builtin_testimonials': 'التوصيات',
        'builtin_faq': 'الأسئلة الشائعة',
        'builtin_cta': 'دعوة للإجراء (CTA)',
    }

    def get_type_display(self):
        return self.SECTION_TYPES.get(self.section_type, self.section_type)

    def __repr__(self):
        return f'<HomeSection {self.section_type} - Order:{self.sort_order}>'
