from datetime import datetime, timedelta
from app import create_app, db
from app.models.user import User
from app.models.home import HeroSection, HomeSection
from app.models.home_content import Feature, Stat, Step, Testimonial, FaqItem
from app.models.plan import Plan
from app.models.category import Category

app = create_app()

with app.app_context():
    db.create_all()

    # ── Admin ──────────────────────────────────────────────
    if not User.query.filter_by(role='admin').first():
        admin = User(
            username='admin',
            email='admin@treeda.com',
            role='admin',
            is_active=True,
            is_verified=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('✅ Admin account created successfully!')
    else:
        print('ℹ️  Admin account already exists.')

    print('📧 Admin login: admin@treeda.com')
    print('🔑 Admin password: admin123')

    # ── HeroSection ───────────────────────────────────────
    if not HeroSection.query.first():
        hero = HeroSection(
            title='مرحباً بكم في المعرض الإلكتروني للمدارس',
            title_ar='مرحباً بكم في المعرض الإلكتروني للمدارس',
            subtitle='منصة متكاملة لعرض المدارس والتعريف بخدماتها',
            description='اكتشف المدارس الحكومية والخاصة والدولية في مكان واحد. تصفح الصور والفيديوهات والأنشطة المدرسية.',
            button1_text='استعرض المدارس',
            button1_link='/schools',
            button1_style='primary',
            button2_text='سجل مدرستك',
            button2_link='/auth/register/school',
            button2_style='outline',
            background_color='#1e1b4b',
            background_type='image',
            is_active=True
        )
        db.session.add(hero)
        db.session.commit()
        print('✅ HeroSection created successfully!')
    else:
        print('ℹ️  HeroSection already exists.')

    # ── HomeSection (built-in) ─────────────────────────────
    builtin_sections = [
        ('builtin_hero', 'القسم الرئيسي', 'Hero', 10),
        ('builtin_stats', 'الإحصائيات', 'Stats', 20),
        ('builtin_features', 'لماذا نحن', 'Why Us', 30),
        ('builtin_categories', 'أقسام المدارس', 'School Categories', 40),
        ('builtin_featured_schools', 'المدارس المميزة', 'Featured Schools', 50),
        ('builtin_gallery', 'معرض الصور', 'Gallery', 60),
        ('builtin_steps', 'خطوات العمل', 'How It Works', 70),
        ('builtin_pricing', 'الباقات والأسعار', 'Pricing Plans', 80),
        ('builtin_testimonials', 'توصيات أولياء الأمور', 'Testimonials', 90),
        ('builtin_faq', 'الأسئلة الشائعة', 'FAQ', 100),
        ('builtin_cta', 'دعوة للتسجيل', 'Call to Action', 110),
    ]

    for section_type, title_ar, title_en, sort_order in builtin_sections:
        existing = HomeSection.query.filter_by(section_type=section_type).first()
        if not existing:
            section = HomeSection(
                section_type=section_type,
                title=title_en,
                title_ar=title_ar,
                sort_order=sort_order,
                is_active=True,
                padding_top=60,
                padding_bottom=60
            )
            db.session.add(section)
            print(f'✅ HomeSection "{section_type}" created!')
        else:
            print(f'ℹ️  HomeSection "{section_type}" already exists.')

    # ── Categories ─────────────────────────────────────────
    categories_data = [
        ('المدارس الحكومية', 'Government Schools', 'government-schools', 'مدارس حكومية متميزة بمناهج وطنية وكوادر تعليمية مؤهلة.', 'Distinguished government schools with national curricula and qualified teaching staff.', 1),
        ('المدارس الخاصة', 'Private Schools', 'private-schools', 'مدارس خاصة تقدم برامج تعليمية متنوعة بمعايير عالمية.', 'Private schools offering diverse educational programs with international standards.', 2),
        ('المدارس العالمية', 'International Schools', 'international-schools', 'مدارس عالمية تتبع مناهج دولية وتمنح شهادات معترف بها.', 'International schools following global curricula and awarding recognized certificates.', 3),
        ('مدارس تحفيظ القرآن', 'Quran Schools', 'quran-schools', 'مدارس متخصصة في تحفيظ القرآن الكريم وتعليم العلوم الشرعية.', 'Specialized schools for Quran memorization and Islamic studies.', 4),
    ]
    for name, name_en, slug, desc, desc_en, sort in categories_data:
        existing = Category.query.filter_by(slug=slug).first()
        if not existing:
            cat = Category(name=name, name_en=name_en, slug=slug, description=desc, sort_order=sort, is_active=True)
            db.session.add(cat)
            print(f'✅ Category "{slug}" created!')
        else:
            print(f'ℹ️  Category "{slug}" already exists.')

    # ── Plans ──────────────────────────────────────────────
    plans_data = [
        ('الباقة الأساسية', 'Basic Plan', 99, 30, 10, 5, 100, 5, False, '#6366f1', 1,
         'ملف تعريفي للمدرسة\nصور وفيديوهات\nدعم فني'),
        ('الباقة المتقدمة', 'Advanced Plan', 249, 30, 30, 15, 500, 15, True, '#f59e0b', 2,
         'كل مميزات الباقة الأساسية\nعدد غير محدود من الصور\nإحصائيات متقدمة\nظهور في المدارس المميزة\nتطبيق مخصص'),
        ('الباقة الاحترافية', 'Professional Plan', 499, 30, 999999, 999999, 2000, 999999, False, '#10b981', 3,
         'كل مميزات الباقة المتقدمة\nمساحة تخزين غير محدودة\nعدد غير محدود من الموظفين\nتقارير واحصائيات شاملة\nدعم فني على مدار الساعة\nاستضافة موقع إلكتروني'),
    ]
    for name, name_en, price, duration, images, videos, storage, employees, featured, color, sort, features in plans_data:
        existing = Plan.query.filter_by(name=name).first()
        if not existing:
            plan = Plan(
                name=name, name_en=name_en, price=price, currency='SAR', duration_days=duration,
                max_images=images, max_videos=videos, storage_mb=storage, max_employees=employees,
                is_featured=featured, color=color, sort_order=sort, is_active=True, features=features
            )
            db.session.add(plan)
            print(f'✅ Plan "{name}" created!')
        else:
            print(f'ℹ️  Plan "{name}" already exists.')

    # ── Features ────────────────────────────────────────────
    features_data = [
        ('search', 'بحث متقدم', 'Advanced Search', 'ابحث عن المدارس بسهولة باستخدام فلتر متعدد الخيارات حسب النوع والموقع والمرحلة الدراسية.',
         'Easily search for schools using a multi-option filter by type, location, and educational stage.', 1),
        ('file-earmark-text', 'ملف تعريفي متكامل', 'Complete Profile', 'كل مدرسة تمتلك ملفاً تعريفياً متكاملاً بالصور والفيديوهات والأنشطة.',
         'Every school has a complete profile with photos, videos, and activities.', 2),
        ('camera', 'معرض وسائط', 'Media Gallery', 'تصفح الصور والفيديوهات عالية الجودة التي تعرض مرافق المدرسة وفعالياتها.',
         'Browse high-quality photos and videos showcasing school facilities and events.', 3),
        ('chat-dots', 'تواصل مباشر', 'Direct Contact', 'تواصل مع إدارة المدرسة مباشرة عبر نموذج الاتصال المدمج.',
         'Contact school administration directly through the built-in contact form.', 4),
        ('credit-card', 'باقات مرنة', 'Flexible Plans', 'اختر الباقة التي تناسب احتياجات مدرستك مع خطط اشتراك مرنة.',
         'Choose the plan that fits your school needs with flexible subscription plans.', 5),
        ('stars', 'مدارس مميزة', 'Featured Schools', 'اكتشف المدارس الأكثر تميزاً وتقييماً من أولياء الأمور والزوار.',
         'Discover the most distinguished and highest-rated schools by parents and visitors.', 6),
    ]
    for icon, title, title_en, desc, desc_en, sort in features_data:
        existing = Feature.query.filter_by(title=title).first()
        if not existing:
            ft = Feature(icon=icon, title=title, title_en=title_en, description=desc, description_en=desc_en, sort_order=sort, is_active=True)
            db.session.add(ft)
            print(f'✅ Feature "{title}" created!')
        else:
            print(f'ℹ️  Feature "{title}" already exists.')

    # ── Stats ──────────────────────────────────────────────
    stats_data = [
        ('mortarboard', '250+', 'مدرسة مسجلة', 'Registered Schools', 1),
        ('people', '15,000+', 'ولي أمر', 'Parents', 2),
        ('images', '8,500+', 'صورة وفيديو', 'Photos & Videos', 3),
        ('award', '98%', 'رضا المستخدمين', 'User Satisfaction', 4),
    ]
    for icon, value, label, label_en, sort in stats_data:
        existing = Stat.query.filter_by(label=label).first()
        if not existing:
            st = Stat(icon=icon, value=value, label=label, label_en=label_en, sort_order=sort, is_active=True)
            db.session.add(st)
            print(f'✅ Stat "{label}" created!')
        else:
            print(f'ℹ️  Stat "{label}" already exists.')

    # ── Steps ──────────────────────────────────────────────
    steps_data = [
        ('person-plus', 'إنشاء حساب', 'Create an Account', 'الخطوة الأولى', 'Step 1',
         'قم بإنشاء حساب جديد كمدرسة أو ولي أمر للانضمام إلى منصتنا.', 'Create a new account as a school or parent to join our platform.', 1),
        ('search', 'اكتشف المدارس', 'Discover Schools', 'الخطوة الثانية', 'Step 2',
         'تصفح قائمة المدارس واستخدم الفلاتر للعثور على المدرسة المناسبة.', 'Browse the school list and use filters to find the right school.', 2),
        ('chat-dots', 'تواصل وتسجيل', 'Connect & Enroll', 'الخطوة الثالثة', 'Step 3',
         'تواصل مع المدرسة مباشرة وقم بتسجيل أبنائك في المدرسة التي تختارها.', 'Contact the school directly and enroll your children in your chosen school.', 3),
    ]
    for icon, title, title_en, tag, tag_en, desc, desc_en, sort in steps_data:
        existing = Step.query.filter_by(title=title).first()
        if not existing:
            st = Step(icon=icon, title=title, title_en=title_en, tag=tag, tag_en=tag_en,
                      description=desc, description_en=desc_en, sort_order=sort, is_active=True)
            db.session.add(st)
            print(f'✅ Step "{title}" created!')
        else:
            print(f'ℹ️  Step "{title}" already exists.')

    # ── Testimonials ───────────────────────────────────────
    testimonials_data = [
        ('أحمد السيد', 'Ahmed Al-Sayed', 'وليّ أمر', 'Parent',
         'منصة رائعة! ساعدتني في العثور على المدرسة المناسبة لأطفالي بكل سهولة. التقييمات والصور كانت مفيدة جداً.',
         'Amazing platform! It helped me find the right school for my children easily. The ratings and photos were very helpful.',
         5, 1),
        ('سارة محمد', 'Sarah Mohammed', 'مديرة مدرسة', 'School Principal',
         'تجربة ممتازة مع المنصة. تمكنّا من عرض مدرستنا بشكل احترافي وجذب أولياء أمور جدد. نظام الاشتراكات مرن ومناسب.',
         'Excellent experience with the platform. We were able to showcase our school professionally and attract new parents. The subscription system is flexible and suitable.',
         5, 2),
        ('خالد العتيبي', 'Khalid Al-Otaibi', 'وليّ أمر', 'Parent',
         'بحثت عن مدارس لابني ووجدت كل ما أحتاجه في مكان واحد. الصور والفيديوهات أعطتني فكرة واضحة عن المدرسة.',
         'I searched for schools for my son and found everything I needed in one place. The photos and videos gave me a clear idea about the school.',
         4, 3),
    ]
    for author, author_en, role, role_en, text, text_en, rating, sort in testimonials_data:
        existing = Testimonial.query.filter_by(author_name=author).first()
        if not existing:
            t = Testimonial(author_name=author, author_name_en=author_en, author_role=role, author_role_en=role_en,
                            text=text, text_en=text_en, rating=rating, is_active=True)
            db.session.add(t)
            print(f'✅ Testimonial "{author}" created!')
        else:
            print(f'ℹ️  Testimonial "{author}" already exists.')

    # ── FAQ Items ──────────────────────────────────────────
    faqs_data = [
        ('ما هي منصة المعرض الإلكتروني للمدارس؟', 'What is the School Exhibition Platform?',
         'منصة إلكترونية تهدف إلى ربط أولياء الأمور بالمدارس من خلال توفير معلومات شاملة وصور وفيديوهات عن كل مدرسة.',
         'An online platform aimed at connecting parents with schools by providing comprehensive information, photos, and videos about each school.',
         1),
        ('كيف يمكنني تسجيل مدرستي في المنصة؟', 'How can I register my school on the platform?',
         'يمكنك التسجيل بالضغط على زر "سجل مدرستك" وملء النموذج. بعد المراجعة والموافقة، سيتم تفعيل حساب المدرسة.',
         'You can register by clicking "Register Your School" and filling out the form. After review and approval, the school account will be activated.',
         2),
        ('هل المنصة مجانية لأولياء الأمور؟', 'Is the platform free for parents?',
         'نعم، المنصة مجانية بالكامل لأولياء الأمور. يمكنكم تصفح المدارس ومشاهدة الصور والفيديوهات والتواصل مع المدارس دون أي رسوم.',
         'Yes, the platform is completely free for parents. You can browse schools, view photos and videos, and contact schools without any fees.',
         3),
        ('ما هي الباقات المتاحة للمدارس؟', 'What plans are available for schools?',
         'نقدم ثلاث باقات: الأساسية (مجانية)، المتقدمة، والاحترافية. كل باقة توفر مميزات متزايدة تناسب احتياجات المدارس المختلفة.',
         'We offer three plans: Basic (free), Advanced, and Professional. Each plan provides increasing features to suit different school needs.',
         4),
        ('كيف يمكنني التواصل مع المدرسة؟', 'How can I contact a school?',
         'يمكنك التواصل مع المدرسة مباشرة من خلال صفحة المدرسة عبر نموذج الاتصال المدمج، أو استخدام معلومات الاتصال المتوفرة في الملف التعريفي.',
         'You can contact the school directly through the school page via the built-in contact form, or use the contact information available in the profile.',
         5),
    ]
    for question, question_en, answer, answer_en, sort in faqs_data:
        existing = FaqItem.query.filter_by(question=question).first()
        if not existing:
            fq = FaqItem(question=question, question_en=question_en, answer=answer, answer_en=answer_en, sort_order=sort, is_active=True)
            db.session.add(fq)
            print(f'✅ FaqItem "{question[:30]}..." created!')
        else:
            print(f'ℹ️  FaqItem "{question[:30]}..." already exists.')

    db.session.commit()
    print('🎉 Seed completed successfully!')
