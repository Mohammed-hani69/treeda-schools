"""Seed AiKnowledge table with comprehensive bilingual Q&A pairs for the AI assistant."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.ai_knowledge import AiKnowledge

KNOWLEDGE = [
    # ───── Platform Overview ─────
    {
        "keywords": "تريدا, تريدا أكسبو, اكسبو, المنصة, about, treeda, treeda expo, expo, platform, what is",
        "answer_ar": "تريدا أكسبو هي المنصة الرائدة في المملكة العربية السعودية لربط أولياء الأمور بالمدارس. نهدف إلى تسهيل عملية البحث عن المدارس المناسبة ومقارنتها والتسجيل فيها إلكترونياً. توفر المنصة معلومات شاملة عن آلاف المدارس في مختلف مدن المملكة.",
        "answer_en": "Treeda Expo is the leading platform in Saudi Arabia connecting parents with schools. We aim to facilitate the process of finding, comparing, and registering in suitable schools online. The platform provides comprehensive information about thousands of schools across the Kingdom's cities.",
        "category": "عام",
        "sort_order": 1
    },
    {
        "keywords": "مميزات, مزايا, خدمات, features, benefits, services, what can I do",
        "answer_ar": "توفر تريدا أكسبو العديد من المميزات: 1) البحث عن المدارس حسب المدينة والنوع والفئة العمرية. 2) مقارنة المدارس من حيث الرسوم والخدمات والتقييمات. 3) مشاهدة صور وفيديوهات حقيقية للمدارس. 4) الاطلاع على أنشطة المدارس وخدماتها. 5) التواصل المباشر مع إدارة المدرسة. 6) الباقات المتنوعة التي تناسب احتياجات المدارس.",
        "answer_en": "Treeda Expo offers many features: 1) Search for schools by city, type, and age group. 2) Compare schools by fees, services, and ratings. 3) View real photos and videos of schools. 4) Browse school activities and services. 5) Direct communication with school administration. 6) Various plans that suit school needs.",
        "category": "عام",
        "sort_order": 2
    },
    {
        "keywords": "مجاني, مجانا, هل المنصة مجانية, free, free platform, is it free",
        "answer_ar": "نعم، تصفح المنصة والبحث عن المدارس مجاني تماماً لأولياء الأمور. يمكنك إنشاء حساب والبحث عن المدارس ومشاهدة ملفاتها بدون أي رسوم. بالنسبة للمدارس، نوفر باقات متنوعة تشمل باقة مجانية للبدء.",
        "answer_en": "Yes, browsing the platform and searching for schools is completely free for parents. You can create an account, search for schools, and view their profiles without any fees. For schools, we offer various plans including a free starter plan.",
        "category": "عام",
        "sort_order": 3
    },

    # ───── Registration & Accounts ─────
    {
        "keywords": "تسجيل, اشتراك, حساب جديد, إنشاء حساب, register, signup, create account, new account",
        "answer_ar": "للتسجيل كولي أمر: 1) اضغط على 'تسجيل' في أعلى الصفحة. 2) اختر 'ولي أمر'. 3) املأ البيانات المطلوبة (الاسم، البريد الإلكتروني، رقم الجوال، كلمة المرور). 4) اضغط 'إنشاء حساب'. للتسجيل كمدرسة: يمكنك التواصل معنا عبر نموذج الاتصال أو الاتصال على الرقم 01097000010.",
        "answer_en": "To register as a parent: 1) Click 'Register' at the top of the page. 2) Choose 'Parent'. 3) Fill in the required information (name, email, phone number, password). 4) Click 'Create Account'. To register as a school: you can contact us via the contact form or call +201097000010.",
        "category": "التسجيل",
        "sort_order": 4
    },
    {
        "keywords": "تسجيل دخول, دخول, login, sign in",
        "answer_ar": "لتسجيل الدخول: 1) اضغط على 'دخول' في أعلى الصفحة. 2) أدخل بريدك الإلكتروني أو اسم المستخدم. 3) أدخل كلمة المرور. 4) اضغط 'تسجيل دخول'. إذا نسيت كلمة المرور، اضغط على 'نسيت كلمة المرور' واتبع التعليمات.",
        "answer_en": "To log in: 1) Click 'Login' at the top of the page. 2) Enter your email or username. 3) Enter your password. 4) Click 'Login'. If you forgot your password, click 'Forgot Password' and follow the instructions.",
        "category": "التسجيل",
        "sort_order": 5
    },
    {
        "keywords": "نسيت كلمة المرور, تغيير كلمة المرور, forget password, reset password, change password",
        "answer_ar": "إذا نسيت كلمة المرور: 1) اضغط على 'دخول'. 2) اضغط على 'نسيت كلمة المرور'. 3) أدخل بريدك الإلكتروني المسجل. 4) ستتلقى رابط إعادة تعيين كلمة المرور على بريدك الإلكتروني (قريباً). يمكنك أيضاً التواصل معنا عبر الهاتف 01097000010 للمساعدة.",
        "answer_en": "If you forgot your password: 1) Click 'Login'. 2) Click 'Forgot Password'. 3) Enter your registered email. 4) You'll receive a password reset link on your email (coming soon). You can also contact us at +201097000010 for assistance.",
        "category": "التسجيل",
        "sort_order": 6
    },
    {
        "keywords": "تعديل البيانات, تعديل الملف الشخصي, تحديث, edit profile, update, change info",
        "answer_ar": "يمكنك تعديل بيانات ملفك الشخصي بعد تسجيل الدخول من خلال الذهاب إلى الإعدادات أو الملف الشخصي من القائمة الجانبية. يمكنك تحديث الاسم، البريد الإلكتروني، رقم الجوال، وصورة الملف الشخصي.",
        "answer_en": "You can edit your profile information after logging in by going to Settings or Profile from the sidebar menu. You can update your name, email, phone number, and profile picture.",
        "category": "التسجيل",
        "sort_order": 7
    },

    # ───── Plans & Pricing ─────
    {
        "keywords": "باقات, خطط, أسعار, Plans, pricing, packages, bronze, silver, gold",
        "answer_ar": "نقدم 3 باقات للمدارس:\n🥉 الباقة البرونزية: مجاناً - عدد غير محدود من الصور، فيديو واحد، مدرّس واحد، تخزين 500 ميجابايت.\n🥈 الباقة الفضية: 299 ريال شهرياً - صور وفيديوهات غير محدودة، 3 مدرسين، تخزين 2 جيجابايت.\n🥇 الباقة الذهبية: 599 ريال شهرياً - كل شيء غير محدود، تخزين 5 جيجابايت + مميزات خاصة.",
        "answer_en": "We offer 3 plans for schools:\n🥉 Bronze: Free - Unlimited images, 1 video, 1 teacher, 500MB storage.\n🥈 Silver: 299 SAR/month - Unlimited images & videos, 3 teachers, 2GB storage.\n🥇 Gold: 599 SAR/month - Everything unlimited, 5GB storage + special features.",
        "category": "الباقات",
        "sort_order": 8
    },
    {
        "keywords": "ترقية الباقة, تغيير الباقة, تطوير الاشتراك, upgrade plan, change plan, subscription upgrade",
        "answer_ar": "لترقية باقتك، تواصل مع إدارة المنصة عبر: 1) الذهاب إلى صفحة الباقات في لوحة تحكم المدرسة. 2) اختيار الباقة التي تريد الترقية إليها. 3) التواصل معنا عبر الهاتف 01097000010 أو البريد الإلكتروني لتأكيد الترقية.",
        "answer_en": "To upgrade your plan, contact platform management via: 1) Go to the Plans page in the school dashboard. 2) Choose the plan you want to upgrade to. 3) Contact us at +201097000010 or via email to confirm the upgrade.",
        "category": "الباقات",
        "sort_order": 9
    },
    {
        "keywords": "إلغاء الاشتراك, إلغاء الباقة, cancel subscription, cancel plan",
        "answer_ar": "يمكنك إلغاء اشتراكك في أي وقت. للقيام بذلك، تواصل معنا عبر الهاتف 01097000010 أو عبر البريد الإلكتروني. سيتم إلغاء الاشتراك في نهاية دورة الفوترة الحالية.",
        "answer_en": "You can cancel your subscription at any time. To do so, contact us at +201097000010 or via email. The subscription will be cancelled at the end of the current billing cycle.",
        "category": "الباقات",
        "sort_order": 10
    },
    {
        "keywords": "طريقة الدفع, وسائل الدفع, دفع, payment, pay, payment methods",
        "answer_ar": "طرق الدفع المتاحة حالياً:\n1) التحويل البنكي.\n2) الدفع نقداً (لمدارس الرياض).\nنعمل حالياً على إضافة المزيد من طرق الدفع مثل بطاقات الائتمان و Apple Pay.",
        "answer_en": "Available payment methods:\n1) Bank transfer.\n2) Cash payment (for Riyadh schools).\nWe are currently working on adding more payment methods like credit cards and Apple Pay.",
        "category": "الباقات",
        "sort_order": 11
    },

    # ───── Schools ─────
    {
        "keywords": "البحث عن مدارس, schools, search, find schools, school search",
        "answer_ar": "للبحث عن المدارس: 1) اذهب إلى صفحة 'المدارس'. 2) استخدم خانة البحث لإدخال اسم المدرسة. 3) استخدم الفلاتر لاختيار المدينة أو النوع أو المرحلة الدراسية. 4) اختر المدرسة المناسبة لعرض ملفها الكامل.",
        "answer_en": "To search for schools: 1) Go to the 'Schools' page. 2) Use the search box to enter the school name. 3) Use filters to select city, type, or educational level. 4) Choose the suitable school to view its full profile.",
        "category": "المدارس",
        "sort_order": 12
    },
    {
        "keywords": "أنواع المدارس, مدارس حكومية, مدارس أهلية, مدارس عالمية, مدارس تحفيظ, government, private, international, quran, school types",
        "answer_ar": "تغطي منصتنا 4 أنواع رئيسية من المدارس:\n1) المدارس الحكومية: تابعة لوزارة التعليم.\n2) المدارس الأهلية: مدارس خاصة.\n3) المدارس العالمية: تقدم مناهج دولية.\n4) مدارس تحفيظ القرآن: تركز على تحفيظ القرآن الكريم.",
        "answer_en": "Our platform covers 4 main types of schools:\n1) Government Schools: Under the Ministry of Education.\n2) Private Schools: Privately owned schools.\n3) International Schools: Offer international curricula.\n4) Quran Schools: Focus on Quran memorization.",
        "category": "المدارس",
        "sort_order": 13
    },
    {
        "keywords": "مدارس الرياض, مدارس جدة, مدارس مكة, مدارس المدينة, مدارس الدمام, مدارس السعودية, riyadh, jeddah, mecca, medina, dammam, cities",
        "answer_ar": "تغطي منصتنا مدارس في جميع مدن المملكة العربية السعودية بما في ذلك: الرياض، جدة، مكة المكرمة، المدينة المنورة، الدمام، الخبر، الطائف، تبوك، بريدة، حائل، نجران، جازان، وأكثر. يمكنك تصفية البحث حسب المدينة لسهولة الوصول.",
        "answer_en": "Our platform covers schools in all cities of Saudi Arabia including: Riyadh, Jeddah, Mecca, Medina, Dammam, Khobar, Taif, Tabuk, Buraidah, Hail, Najran, Jazan, and more. You can filter your search by city for easy access.",
        "category": "المدارس",
        "sort_order": 14
    },
    {
        "keywords": "تسجيل طالب, تسجيل ابن, قبول, admission, register student, enroll, registration for child",
        "answer_ar": "للاستفسار عن تسجيل الطلاب والتقديم، يمكنك: 1) الدخول إلى صفحة المدرسة. 2) الاطلاع على معلومات الاتصال الخاصة بالمدرسة. 3) التواصل مباشرة مع إدارة المدرسة. المنصة حالياً لا توفر التقديم الإلكتروني المباشر، ولكننا نعمل على إضافته قريباً.",
        "answer_en": "To inquire about student registration and admission: 1) Go to the school page. 2) View the school's contact information. 3) Contact the school administration directly. The platform currently doesn't offer direct online application, but we are working on adding it soon.",
        "category": "المدارس",
        "sort_order": 15
    },
    {
        "keywords": "رسوم المدارس, مصاريف, تكاليف, school fees, tuition, costs",
        "answer_ar": "تختلف رسوم المدارس حسب المدينة والنوع والمرحلة الدراسية. يمكنك الاطلاع على معلومات الرسوم في صفحة كل مدرسة ضمن قسم 'الرسوم'. للمزيد من التفاصيل، تواصل مع إدارة المدرسة مباشرة.",
        "answer_en": "School fees vary by city, type, and educational level. You can view fee information on each school's page under the 'Fees' section. For more details, contact the school administration directly.",
        "category": "المدارس",
        "sort_order": 16
    },
    {
        "keywords": "مدرسة, تسجيل مدرسة, إضافة مدرسة, إدراج مدرسة, add school, register school, list school",
        "answer_ar": "لتسجيل مدرستك في المنصة: 1) تواصل معنا عبر نموذج الاتصال في الصفحة الرئيسية. 2) أو اتصل بنا على الرقم 01097000010. 3) أو راسلنا على البريد الإلكتروني. سنقوم بمساعدتك في إنشاء حساب المدرسة واختيار الباقة المناسبة.",
        "answer_en": "To register your school on the platform: 1) Contact us via the contact form on the homepage. 2) Or call us at +201097000010. 3) Or email us. We will help you create a school account and choose the right plan.",
        "category": "المدارس",
        "sort_order": 17
    },

    # ───── Parent Features ─────
    {
        "keywords": "ولي أمر, أولياء الأمور, parent, parents, guardian",
        "answer_ar": "كولي أمر، يمكنك من خلال المنصة: البحث عن المدارس المناسبة لأبنائك، مقارنة المدارس بجانب بعض، مشاهدة الصور والفيديوهات الحقيقية، الاطلاع على أنشطة المدرسة وخدماتها، التواصل مع إدارة المدرسة، وحفظ المدارس المفضلة.",
        "answer_en": "As a parent, through the platform you can: search for suitable schools for your children, compare schools side by side, view real photos and videos, browse school activities and services, contact school administration, and save favorite schools.",
        "category": "أولياء الأمور",
        "sort_order": 18
    },
    {
        "keywords": "المدارس المفضلة, حفظ المدارس, مفضلة, favorites, save schools, wishlist",
        "answer_ar": "يمكنك إضافة المدارس إلى المفضلة للرجوع إليها لاحقاً. اضغط على أيقونة القلب في صفحة المدرسة أو في نتائج البحث. يمكنك الوصول إلى قائمة المفضلة من صفحة 'المفضلة' في حسابك.",
        "answer_en": "You can add schools to your favorites for later reference. Click the heart icon on the school page or in search results. You can access your favorites list from the 'Favorites' page in your account.",
        "category": "أولياء الأمور",
        "sort_order": 19
    },
    {
        "keywords": "مقارنة المدارس, مقارنة, compare, comparison",
        "answer_ar": "يمكنك مقارنة المدارس بجانب بعضها البعض. اختر المدارس التي تريد مقارنتها ثم اضغط على 'مقارنة'. ستظهر لك المعلومات جنباً إلى جنب لتسهيل اتخاذ القرار المناسب.",
        "answer_en": "You can compare schools side by side. Select the schools you want to compare and click 'Compare'. Information will appear side by side to help you make the right decision.",
        "category": "أولياء الأمور",
        "sort_order": 20
    },

    # ───── Technical ─────
    {
        "keywords": "مشكلة تقنية, مشكلة, خطأ, bug, error, technical issue, problem, not working",
        "answer_ar": "إذا واجهتك أي مشكلة تقنية، يرجى المحاولة أولاً بـ: 1) تحديث الصفحة (F5). 2) مسح كاش المتصفح (Cache). 3) تجربة متصفح آخر. إذا استمرت المشكلة، تواصل معنا عبر الهاتف 01097000010 أو عبر نموذج الاتصال مع توضيح المشكلة بالتفصيل.",
        "answer_en": "If you encounter any technical issue, please first try: 1) Refreshing the page (F5). 2) Clearing your browser cache. 3) Trying another browser. If the problem persists, contact us at +201097000010 or via the contact form with a detailed description.",
        "category": "تقني",
        "sort_order": 21
    },
    {
        "keywords": "تطبيق جوال, تطبيق, mobile app, app, ios, android, iphone",
        "answer_ar": "حالياً المنصة متاحة عبر المتصفح (Web App). نحن نعمل على تطوير تطبيقات الجوال لأنظمة iOS و Android وسيتم إطلاقها قريباً بإذن الله.",
        "answer_en": "Currently the platform is available as a web app. We are developing mobile applications for iOS and Android which will be launched soon, God willing.",
        "category": "تقني",
        "sort_order": 22
    },
    {
        "keywords": "اللغة, تغيير اللغة, English, العربية, language, change language, switch language",
        "answer_ar": "يمكنك تغيير لغة المنصة بالضغط على أيقونة اللغة في أعلى الصفحة. المنصة تدعم اللغتين العربية والإنجليزية بشكل كامل.",
        "answer_en": "You can change the platform language by clicking the language icon at the top of the page. The platform fully supports both Arabic and English.",
        "category": "تقني",
        "sort_order": 23
    },

    # ───── Contact & Support ─────
    {
        "keywords": "اتصال, تواصل, دعم, contact, support, help, customer service",
        "answer_ar": "يمكنك التواصل معنا عبر:\n📞 الهاتف: 01097000010\n📧 البريد الإلكتروني: support@treeda-expo.com\n💬 واتساب: +201097000010\n📍 العنوان: الرياض، المملكة العربية السعودية\nنحن متاحون من الأحد إلى الخميس، 9 صباحاً - 5 مساءً.",
        "answer_en": "You can contact us via:\n📞 Phone: +201097000010\n📧 Email: support@treeda-expo.com\n💬 WhatsApp: +201097000010\n📍 Address: Riyadh, Saudi Arabia\nWe are available Sunday to Thursday, 9 AM - 5 PM.",
        "category": "الدعم",
        "sort_order": 24
    },
    {
        "keywords": "شكوى, اقتراح, complaint, suggestion, feedback",
        "answer_ar": "نرحب باقتراحاتك وشكواك. يمكنك مراسلتنا عبر نموذج الاتصال في الموقع أو عبر البريد الإلكتروني support@treeda-expo.com. يتم الرد على جميع الاستفسارات خلال 24 ساعة.",
        "answer_en": "We welcome your suggestions and complaints. You can contact us via the contact form on the website or via email at support@treeda-expo.com. All inquiries are answered within 24 hours.",
        "category": "الدعم",
        "sort_order": 25
    },

    # ───── Categories ─────
    {
        "keywords": "أقسام, تصنيفات المدارس, categories, school categories",
        "answer_ar": "تصنف المدارس في منصتنا إلى 4 أقسام رئيسية:\n1) المدارس الحكومية\n2) المدارس الأهلية\n3) المدارس العالمية\n4) مدارس تحفيظ القرآن\nيمكنك تصفية البحث حسب القسم الذي تفضله.",
        "answer_en": "Schools on our platform are classified into 4 main categories:\n1) Government Schools\n2) Private Schools\n3) International Schools\n4) Quran Memorization Schools\nYou can filter your search by your preferred category.",
        "category": "عام",
        "sort_order": 26
    },

    # ───── Media & Content ─────
    {
        "keywords": "صور, فيديو, رفع صور, رفع فيديو, media, upload, images, videos, photos",
        "answer_ar": "بعد تسجيل الدخول إلى حساب المدرسة، يمكنك من لوحة التحكم:\n1) الذهاب إلى قسم 'الوسائط'.\n2) رفع الصور والفيديوهات الخاصة بمدرستك.\n3) الحد المسموح يعتمد على باقتك (الباقة البرونزية: صور غير محدودة وفيديو واحد).",
        "answer_en": "After logging into your school account, from the dashboard:\n1) Go to the 'Media' section.\n2) Upload your school's images and videos.\n3) The allowed limit depends on your plan (Bronze: unlimited images and 1 video).",
        "category": "المدارس",
        "sort_order": 27
    },

    # ───── School Dashboard ─────
    {
        "keywords": "لوحة تحكم المدرسة, school dashboard, school control panel",
        "answer_ar": "لوحة تحكم المدرسة تمكنك من: إدارة الملف الشخصي للمدرسة، رفع الصور والفيديوهات، إضافة الأنشطة والخدمات، إدارة المعلمين، متابعة الاستخدام والباقة، وعرض الإحصائيات.",
        "answer_en": "The school dashboard allows you to: manage the school profile, upload images and videos, add activities and services, manage teachers, monitor usage and plan, and view statistics.",
        "category": "المدارس",
        "sort_order": 28
    },
    {
        "keywords": "معلم, معلمين, كادر تدريسي, teacher, teachers, staff",
        "answer_ar": "يمكن إضافة المعلمين من لوحة تحكم المدرسة. عدد المعلمين المسموح به يعتمد على الباقة: البرونزية (مدرس واحد)، الفضية (3 مدرسين)، الذهبية (غير محدود).",
        "answer_en": "Teachers can be added from the school dashboard. The number of allowed teachers depends on your plan: Bronze (1 teacher), Silver (3 teachers), Gold (unlimited).",
        "category": "المدارس",
        "sort_order": 29
    },
    {
        "keywords": "نشاط, أنشطة مدرسية, خدمات, activities, school activities, services",
        "answer_ar": "يمكن إضافة الأنشطة والخدمات المدرسية من لوحة تحكم المدرسة. أضف اسم النشاط، وصف مختصر، وصورة إن وجدت. ستعرض هذه الأنشطة في صفحة المدرسة لأولياء الأمور.",
        "answer_en": "School activities and services can be added from the school dashboard. Add the activity name, brief description, and an image if available. These activities will be displayed on the school page for parents.",
        "category": "المدارس",
        "sort_order": 30
    },

    # ───── AI Assistant / Chatbot ─────
    {
        "keywords": "المساعد الذكي, الذكاء الاصطناعي, الذكاء, ai, chatbot, chat bot, ai assistant, مساعد, بوت, robot, assistant",
        "answer_ar": "أنا المساعد الذكي لتريدا أكسبو 🤖! أستطيع الإجابة عن أسئلتك حول المنصة، الباقات، التسجيل، المدارس، وأي استفسار آخر. فقط اكتب سؤالك وسأحاول مساعدتك. إذا لم أتمكن من الإجابة، يمكنك التواصل مع فريق الدعم البشري.",
        "answer_en": "I am the Treeda Expo AI assistant 🤖! I can answer your questions about the platform, plans, registration, schools, and any other inquiries. Just type your question and I'll try to help. If I can't answer, you can contact the human support team.",
        "category": "عام",
        "sort_order": 31
    },
    {
        "keywords": "كيف يعمل المساعد الذكي, كيف يعمل الذكاء الاصطناعي, كيف يعمل البوت, كيف تعمل, how does ai work, how does chatbot work, how do you work",
        "answer_ar": "أعمل من خلال البحث في قاعدة معرفية تضم أكثر من 30 سؤالاً وإجابة عن المنصة. عندما تسألني سؤالاً، أبحث عن الكلمات المفتاحية المطابقة وأعرض لك الإجابة المناسبة. أنا لا أستخدم ذكاءً اصطناعياً توليدياً (مثل ChatGPT)، بل أعتمد على قاعدة معرفية محدثة باستمرار من قبل إدارة المنصة.",
        "answer_en": "I work by searching a knowledge base of over 30 questions and answers about the platform. When you ask me a question, I search for matching keywords and show you the appropriate answer. I don't use generative AI (like ChatGPT), but rely on a knowledge base that is constantly updated by the platform administration.",
        "category": "عام",
        "sort_order": 32
    },
    {
        "keywords": "ماذا تستطيع, ماذا يمكنك, ماذا تعرف, ماذا تفعل, what can you do, what do you know, capabilities, features of ai",
        "answer_ar": "أستطيع الإجابة عن أسئلتك في هذه المجالات:\n1) معلومات عن المنصة ومميزاتها.\n2) طريقة التسجيل كولي أمر أو مدرسة.\n3) الباقات والأسعار وطرق الدفع.\n4) البحث عن المدارس وأنواعها.\n5) الأنشطة والخدمات والوسائط.\n6) معلومات الاتصال والدعم الفني.\n7) أي استفسار آخر عن المنصة!",
        "answer_en": "I can answer your questions in these areas:\n1) Platform information and features.\n2) Registration as a parent or school.\n3) Plans, pricing, and payment methods.\n4) School search and types.\n5) Activities, services, and media.\n6) Contact information and technical support.\n7) Any other platform-related inquiry!",
        "category": "عام",
        "sort_order": 33
    },
]


def seed():
    app = create_app()
    with app.app_context():
        existing = AiKnowledge.query.count()
        if existing > 0:
            print(f'Found {existing} existing knowledge entries. Clearing...')
            AiKnowledge.query.delete()
            db.session.commit()

        for i, item in enumerate(KNOWLEDGE):
            entry = AiKnowledge(
                keywords=item['keywords'],
                answer_ar=item['answer_ar'],
                answer_en=item['answer_en'],
                category=item['category'],
                sort_order=item['sort_order'],
                is_active=True
            )
            db.session.add(entry)

        db.session.commit()
        total = AiKnowledge.query.count()
        print(f'✅ Seeded {total} AI knowledge entries successfully!')

        # Print categories
        cats = db.session.query(AiKnowledge.category).distinct().all()
        print(f'\nCategories ({len(cats)}):')
        for c in cats:
            cnt = AiKnowledge.query.filter_by(category=c[0]).count()
            print(f'  - {c[0]}: {cnt} entries')


if __name__ == '__main__':
    seed()
