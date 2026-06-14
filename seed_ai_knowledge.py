"""Seed AiKnowledge table with comprehensive bilingual Q&A pairs for the AI assistant."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.ai_knowledge import AiKnowledge

KNOWLEDGE = [
    # ═══════════════════════════════════════════
    # عام (General)
    # ═══════════════════════════════════════════
    {
        "keywords": "تريدا, تريدا أكسبو, اكسبو, المنصة, about, treeda, treeda expo, expo, platform, what is, ما هي, نبذة, تعريف",
        "answer_ar": "تريدا أكسبو هي المنصة المصرية الرائدة لربط أولياء الأمور بالمدارس. نهدف إلى تسهيل عملية البحث عن المدارس المناسبة ومقارنتها والتسجيل فيها إلكترونياً. توفر المنصة معلومات شاملة عن آلاف المدارس في مختلف المدن المصرية.",
        "answer_en": "Treeda Expo is the leading Egyptian platform connecting parents with schools. We aim to facilitate the process of finding, comparing, and registering in suitable schools online. The platform provides comprehensive information about thousands of schools across Egyptian cities.",
        "category": "عام",
        "sort_order": 1
    },
    {
        "keywords": "مميزات, مزايا, خدمات, features, benefits, services, what can I do, إيه اللي بتقدمه, إيه المميزات",
        "answer_ar": "توفر تريدا أكسبو العديد من المميزات: 1) البحث عن المدارس حسب المحافظة والنوع والمرحلة الدراسية. 2) مقارنة المدارس من حيث المصروفات والخدمات والتقييمات. 3) مشاهدة صور وفيديوهات حقيقية للمدارس. 4) الاطلاع على أنشطة المدرسة وخدماتها. 5) التواصل المباشر مع إدارة المدرسة. 6) الباقات المتنوعة التي تناسب احتياجات المدارس.",
        "answer_en": "Treeda Expo offers many features: 1) Search for schools by governorate, type, and educational stage. 2) Compare schools by fees, services, and ratings. 3) View real photos and videos of schools. 4) Browse school activities and services. 5) Direct communication with school administration. 6) Various plans that suit school needs.",
        "category": "عام",
        "sort_order": 2
    },
    {
        "keywords": "مجاني, مجانا, هل المنصة مجانية, free, free platform, is it free, مجانية, بالمجان",
        "answer_ar": "نعم، تصفح المنصة والبحث عن المدارس مجاني تماماً لأولياء الأمور. يمكنك إنشاء حساب والبحث عن المدارس ومشاهدة ملفاتها بدون أي رسوم. بالنسبة للمدارس، نوفر باقات متنوعة تشمل باقة مجانية للبدء.",
        "answer_en": "Yes, browsing the platform and searching for schools is completely free for parents. You can create an account, search for schools, and view their profiles without any fees. For schools, we offer various plans including a free starter plan.",
        "category": "عام",
        "sort_order": 3
    },
    {
        "keywords": "أقسام, تصنيفات المدارس, categories, school categories, أنواع, تصنيف",
        "answer_ar": "تصنف المدارس في منصتنا إلى 4 أقسام رئيسية:\n1) المدارس الحكومية\n2) المدارس الأهلية (الخاصة)\n3) المدارس الدولية\n4) مدارس تحفيظ القرآن\nيمكنك تصفية البحث حسب القسم الذي تفضله.",
        "answer_en": "Schools on our platform are classified into 4 main categories:\n1) Government Schools\n2) Private Schools\n3) International Schools\n4) Quran Memorization Schools\nYou can filter your search by your preferred category.",
        "category": "عام",
        "sort_order": 4
    },
    {
        "keywords": "المساعد الذكي, الذكاء الاصطناعي, الذكاء, ai, chatbot, chat bot, ai assistant, مساعد, بوت, robot, assistant, البوت, الشات بوت",
        "answer_ar": "أنا المساعد الذكي لتريدا أكسبو 🤖! أستطيع الإجابة عن أسئلتك حول المنصة، الباقات، التسجيل، المدارس، المناهج، وأي استفسار آخر. فقط اكتب سؤالك وسأحاول مساعدتك. إذا لم أتمكن من الإجابة، يمكنك التواصل مع فريق الدعم البشري.",
        "answer_en": "I am the Treeda Expo AI assistant 🤖! I can answer your questions about the platform, plans, registration, schools, curricula, and any other inquiries. Just type your question and I'll try to help. If I can't answer, you can contact the human support team.",
        "category": "عام",
        "sort_order": 5
    },
    {
        "keywords": "كيف يعمل المساعد الذكي, كيف يعمل الذكاء الاصطناعي, كيف يعمل البوت, كيف تعمل, how does ai work, how does chatbot work, how do you work, آلية العمل, طريقة العمل",
        "answer_ar": "أعمل من خلال البحث في قاعدة معرفية تضم أكثر من 80 سؤالاً وإجابة عن المنصة. عندما تسألني سؤالاً، أبحث عن الكلمات المفتاحية المطابقة وأعرض لك الإجابة المناسبة. أنا لا أستخدم ذكاءً اصطناعياً توليدياً (مثل ChatGPT)، بل أعتمد على قاعدة معرفية محدثة باستمرار من قبل إدارة المنصة.",
        "answer_en": "I work by searching a knowledge base of over 80 questions and answers about the platform. When you ask me a question, I search for matching keywords and show you the appropriate answer. I don't use generative AI (like ChatGPT), but rely on a knowledge base that is constantly updated by the platform administration.",
        "category": "عام",
        "sort_order": 6
    },
    {
        "keywords": "ماذا تستطيع, ماذا يمكنك, ماذا تعرف, ماذا تفعل, what can you do, what do you know, capabilities, features of ai, إمكانيات, قدرات",
        "answer_ar": "أستطيع الإجابة عن أسئلتك في هذه المجالات:\n1) معلومات عن المنصة ومميزاتها.\n2) طريقة التسجيل كولي أمر أو مدرسة.\n3) الباقات والأسعار وطرق الدفع.\n4) البحث عن المدارس وأنواعها.\n5) المناهج الدراسية في مصر.\n6) الأنشطة والخدمات والوسائط.\n7) معلومات الاتصال والدعم الفني.\n8) أي استفسار آخر عن المنصة!",
        "answer_en": "I can answer your questions in these areas:\n1) Platform information and features.\n2) Registration as a parent or school.\n3) Plans, pricing, and payment methods.\n4) School search and types.\n5) Curricula in Egypt.\n6) Activities, services, and media.\n7) Contact information and technical support.\n8) Any other platform-related inquiry!",
        "category": "عام",
        "sort_order": 7
    },
    {
        "keywords": "منصة مصرية, مصرية, made in egypt, egyptian platform, هل المنصة مصرية, الشركة, عن الشركة, المؤسس",
        "answer_ar": "نعم، تريدا أكسبو هي منصة مصرية 100% 🏆. تم تطويرها وتشغيلها من مصر لتخدم المجتمع التعليمي المصري. فريق العمل مصري بالكامل ونفخر بأننا نقدم خدمة متميزة للمدارس وأولياء الأمور في جميع المحافظات المصرية.",
        "answer_en": "Yes, Treeda Expo is a 100% Egyptian platform 🏆. It was developed and operated from Egypt to serve the Egyptian educational community. The team is entirely Egyptian and we are proud to provide distinguished service to schools and parents across all Egyptian governorates.",
        "category": "عام",
        "sort_order": 8
    },

    # ═══════════════════════════════════════════
    # التسجيل (Registration)
    # ═══════════════════════════════════════════
    {
        "keywords": "تسجيل, اشتراك, حساب جديد, إنشاء حساب, register, signup, create account, new account, التسجيل, فتح حساب, إنشاء حساب جديد",
        "answer_ar": "للتسجيل كولي أمر:\n1) اضغط على 'تسجيل' في أعلى الصفحة.\n2) اختر 'ولي أمر'.\n3) املأ البيانات المطلوبة (الاسم، البريد الإلكتروني، رقم الجوال، كلمة المرور).\n4) اضغط 'إنشاء حساب'.\nللتسجيل كمدرسة: يمكنك التواصل معنا عبر نموذج الاتصال أو الاتصال على الرقم 01097000010.",
        "answer_en": "To register as a parent:\n1) Click 'Register' at the top of the page.\n2) Choose 'Parent'.\n3) Fill in the required information (name, email, phone number, password).\n4) Click 'Create Account'.\nTo register as a school: contact us via the contact form or call +201097000010.",
        "category": "التسجيل",
        "sort_order": 9
    },
    {
        "keywords": "تسجيل دخول, دخول, login, sign in, دخول الحساب, تسجيل الدخول",
        "answer_ar": "لتسجيل الدخول:\n1) اضغط على 'دخول' في أعلى الصفحة.\n2) أدخل بريدك الإلكتروني أو اسم المستخدم.\n3) أدخل كلمة المرور.\n4) اضغط 'تسجيل دخول'.\nإذا نسيت كلمة المرور، اضغط على 'نسيت كلمة المرور' واتبع التعليمات.",
        "answer_en": "To log in:\n1) Click 'Login' at the top of the page.\n2) Enter your email or username.\n3) Enter your password.\n4) Click 'Login'.\nIf you forgot your password, click 'Forgot Password' and follow the instructions.",
        "category": "التسجيل",
        "sort_order": 10
    },
    {
        "keywords": "نسيت كلمة المرور, تغيير كلمة المرور, forget password, reset password, change password, ضعت كلمة السر, غير كلمة السر, إعادة تعيين",
        "answer_ar": "إذا نسيت كلمة المرور:\n1) اضغط على 'دخول'.\n2) اضغط على 'نسيت كلمة المرور'.\n3) أدخل بريدك الإلكتروني المسجل.\n4) ستتلقى رابط إعادة تعيين كلمة المرور على بريدك الإلكتروني.\nيمكنك أيضاً التواصل معنا عبر الهاتف 01097000010 للمساعدة.",
        "answer_en": "If you forgot your password:\n1) Click 'Login'.\n2) Click 'Forgot Password'.\n3) Enter your registered email.\n4) You'll receive a password reset link on your email.\nYou can also contact us at +201097000010 for assistance.",
        "category": "التسجيل",
        "sort_order": 11
    },
    {
        "keywords": "تعديل البيانات, تعديل الملف الشخصي, تحديث, edit profile, update, change info, تغيير البيانات, تعديل الحساب",
        "answer_ar": "يمكنك تعديل بيانات ملفك الشخصي بعد تسجيل الدخول من خلال الذهاب إلى الإعدادات أو الملف الشخصي من القائمة الجانبية. يمكنك تحديث الاسم، البريد الإلكتروني، رقم الجوال، وصورة الملف الشخصي.",
        "answer_en": "You can edit your profile information after logging in by going to Settings or Profile from the sidebar menu. You can update your name, email, phone number, and profile picture.",
        "category": "التسجيل",
        "sort_order": 12
    },
    {
        "keywords": "حذف الحساب, إلغاء الحساب, delete account, remove account, حذف, إلغاء العضوية",
        "answer_ar": "إذا كنت ترغب في حذف حسابك نهائياً، يرجى التواصل مع فريق الدعم عبر البريد الإلكتروني support@treeda-expo.com أو عبر الهاتف 01097000010. سيتم حذف جميع بياناتك خلال 14 يوماً من تاريخ الطلب.",
        "answer_en": "If you wish to delete your account permanently, please contact the support team via email at support@treeda-expo.com or by phone at +201097000010. All your data will be deleted within 14 days of the request.",
        "category": "التسجيل",
        "sort_order": 13
    },
    {
        "keywords": "أنواع الحسابات, حساب المدرسة, حساب ولي أمر, حساب إداري, account types, school account, parent account, admin account, الفرق بين الحسابات",
        "answer_ar": "توفر المنصة 3 أنواع من الحسابات:\n1) حساب ولي أمر: للبحث عن المدارس ومقارنتها وحفظ المفضلة.\n2) حساب مدرسة: لإدارة الملف الشخصي للمدرسة ورفع الصور والفيديوهات.\n3) حساب إداري: لإدارة المنصة والمستخدمين والباقات.\nيمكنك اختيار نوع الحساب المناسب عند التسجيل.",
        "answer_en": "The platform offers 3 types of accounts:\n1) Parent Account: to search for schools, compare them, and save favorites.\n2) School Account: to manage the school profile and upload images and videos.\n3) Admin Account: to manage the platform, users, and plans.\nYou can choose the appropriate account type when registering.",
        "category": "التسجيل",
        "sort_order": 14
    },

    # ═══════════════════════════════════════════
    # الباقات (Plans & Pricing)
    # ═══════════════════════════════════════════
    {
        "keywords": "باقات, خطط, أسعار, Plans, pricing, packages, bronze, silver, gold, برونزي, فضية, ذهبية, الأسعار, التكلفة",
        "answer_ar": "نقدم 3 باقات للمدارس:\n🥉 الباقة البرونزية: مجاناً - صور غير محدودة، فيديو واحد، مدرّس واحد، تخزين 500 ميجابايت.\n🥈 الباقة الفضية: 1000 جنيه شهرياً - صور وفيديوهات غير محدودة، 3 مدرسين، تخزين 2 جيجابايت.\n🥇 الباقة الذهبية: 2000 جنيه شهرياً - كل شيء غير محدود، تخزين 5 جيجابايت + مميزات خاصة.",
        "answer_en": "We offer 3 plans for schools:\n🥉 Bronze: Free - Unlimited images, 1 video, 1 teacher, 500MB storage.\n🥈 Silver: 1000 EGP/month - Unlimited images & videos, 3 teachers, 2GB storage.\n🥇 Gold: 2000 EGP/month - Everything unlimited, 5GB storage + special features.",
        "category": "الباقات",
        "sort_order": 15
    },
    {
        "keywords": "ترقية الباقة, تغيير الباقة, تطوير الاشتراك, upgrade plan, change plan, subscription upgrade, تطوير الباقة, الترقية",
        "answer_ar": "لترقية باقتك، تواصل مع إدارة المنصة عبر:\n1) الذهاب إلى صفحة الباقات في لوحة تحكم المدرسة.\n2) اختيار الباقة التي تريد الترقية إليها.\n3) التواصل معنا عبر الهاتف 01097000010 أو البريد الإلكتروني لتأكيد الترقية.",
        "answer_en": "To upgrade your plan, contact platform management via:\n1) Go to the Plans page in the school dashboard.\n2) Choose the plan you want to upgrade to.\n3) Contact us at +201097000010 or via email to confirm the upgrade.",
        "category": "الباقات",
        "sort_order": 16
    },
    {
        "keywords": "إلغاء الاشتراك, إلغاء الباقة, cancel subscription, cancel plan, إلغاء, إنهاء الاشتراك",
        "answer_ar": "يمكنك إلغاء اشتراكك في أي وقت. للقيام بذلك، تواصل معنا عبر الهاتف 01097000010 أو عبر البريد الإلكتروني. سيتم إلغاء الاشتراك في نهاية دورة الفوترة الحالية.",
        "answer_en": "You can cancel your subscription at any time. To do so, contact us at +201097000010 or via email. The subscription will be cancelled at the end of the current billing cycle.",
        "category": "الباقات",
        "sort_order": 17
    },
    {
        "keywords": "طريقة الدفع, وسائل الدفع, دفع, payment, pay, payment methods, السداد, الدفع الإلكتروني, فودافون كاش, كاش, تحويل بنكي",
        "answer_ar": "طرق الدفع المتاحة حالياً:\n1) التحويل البنكي.\n2) فودافون كاش.\n3) إي فواتير.\nنعمل حالياً على إضافة المزيد من طرق الدفع مثل بطاقات الائتمان وApple Pay.",
        "answer_en": "Available payment methods:\n1) Bank transfer.\n2) Vodafone Cash.\n3) E-Fawateer.\nWe are currently working on adding more payment methods like credit cards and Apple Pay.",
        "category": "الباقات",
        "sort_order": 18
    },
    {
        "keywords": "فاتورة, الفاتورة, إيصال, invoice, billing, receipt, الفوترة",
        "answer_ar": "يمكنك الحصول على فاتورة اشتراكك من لوحة تحكم المدرسة في قسم 'الفواتير'. سيتم إرسال نسخة من الفاتورة على بريدك الإلكتروني المسجل بعد كل عملية دفع.",
        "answer_en": "You can get your subscription invoice from the school dashboard in the 'Invoices' section. A copy of the invoice will be sent to your registered email after each payment.",
        "category": "الباقات",
        "sort_order": 19
    },
    {
        "keywords": "فترة تجريبية, تجربة مجانية, trial, free trial, جرب مجانا, تجربة, نسخة تجريبية",
        "answer_ar": "نعم، نوفر فترة تجريبية مجانية للمدارس الجديدة لمدة 14 يوماً على الباقة الفضية والذهبية. يمكنك تجربة جميع المميزات قبل الاشتراك. تواصل معنا للاستفادة من العرض.",
        "answer_en": "Yes, we offer a free 14-day trial period for new schools on the Silver and Gold plans. You can try all features before subscribing. Contact us to take advantage of the offer.",
        "category": "الباقات",
        "sort_order": 20
    },
    {
        "keywords": "مقارنة الباقات, مقارنة الخطط, مقارنة, plan comparison, مقارنة الأسعار, أيهما أفضل, إيه أفضل باقة",
        "answer_ar": "الباقة البرونزية مناسبة للمدارس الصغيرة التي تبدأ رحلتها مع المنصة. الباقة الفضية مثالية للمدارس متوسطة الحجم. الباقة الذهبية مخصصة للمدارس الكبيرة التي تريد أقصى استفادة. يمكنك التواصل معنا لمساعدتك في اختيار الباقة المناسبة.",
        "answer_en": "The Bronze plan is suitable for small schools starting their journey with the platform. The Silver plan is ideal for medium-sized schools. The Gold plan is for large schools that want maximum benefit. Contact us to help you choose the right plan.",
        "category": "الباقات",
        "sort_order": 21
    },

    # ═══════════════════════════════════════════
    # المدارس (Schools)
    # ═══════════════════════════════════════════
    {
        "keywords": "البحث عن مدارس, schools, search, find schools, school search, ابحث, دوّر على مدارس, بحث متقدم",
        "answer_ar": "للبحث عن المدارس:\n1) اذهب إلى صفحة 'المدارس'.\n2) استخدم خانة البحث لإدخال اسم المدرسة.\n3) استخدم الفلاتر لاختيار المحافظة أو النوع أو المرحلة الدراسية.\n4) اختر المدرسة المناسبة لعرض ملفها الكامل.",
        "answer_en": "To search for schools:\n1) Go to the 'Schools' page.\n2) Use the search box to enter the school name.\n3) Use filters to select governorate, type, or educational stage.\n4) Choose the suitable school to view its full profile.",
        "category": "المدارس",
        "sort_order": 22
    },
    {
        "keywords": "أنواع المدارس, مدارس حكومية, مدارس أهلية, مدارس عالمية, مدارس تحفيظ, government, private, international, quran, school types, أنواع, أنواع المدارس في مصر",
        "answer_ar": "تغطي منصتنا عدة أنواع من المدارس في مصر:\n1) المدارس الحكومية: تابعة لوزارة التربية والتعليم.\n2) المدارس الخاصة (الأهلية): مدارس خاصة بمصروفات دراسية.\n3) المدارس الدولية: تقدم مناهج أجنبية (بريطاني، أمريكي، فرنسي، ألماني).\n4) مدارس تحفيظ القرآن: تركز على تحفيظ القرآن الكريم.\n5) المدارس التجريبية: مدارس حكومية متميزة بلغات أجنبية.\n6) المدارس الرسمية للغات: مدارس حكومية تدرس باللغة الإنجليزية.",
        "answer_en": "Our platform covers several types of schools in Egypt:\n1) Government Schools: Under the Ministry of Education.\n2) Private Schools: Privately owned with tuition fees.\n3) International Schools: Offer foreign curricula (British, American, French, German).\n4) Quran Schools: Focus on Quran memorization.\n5) Experimental Schools: Distinguished government schools with foreign languages.\n6) Official Language Schools: Government schools taught in English.",
        "category": "المدارس",
        "sort_order": 23
    },
    {
        "keywords": "مدارس القاهرة, مدارس الإسكندرية, مدارس الجيزة, مدارس مصر, محافظات, cairo, alexandria, giza, egyptian cities, governorates, محافظة, مدن مصر, مدارس المحافظات",
        "answer_ar": "تغطي منصتنا مدارس في جميع محافظات مصر بما في ذلك: القاهرة، الإسكندرية، الجيزة، المنصورة، طنطا، أسيوط، الزقازيق، السويس، الإسماعيلية، الأقصر، أسوان، بورسعيد، دمياط، كفر الشيخ، بنها، شبين الكوم، المنيا، سوهاج، قنا، الغردقة، 6 أكتوبر، وأكثر. يمكنك تصفية البحث حسب المحافظة لسهولة الوصول.",
        "answer_en": "Our platform covers schools in all Egyptian governorates including: Cairo, Alexandria, Giza, Mansoura, Tanta, Assiut, Zagazig, Suez, Ismailia, Luxor, Aswan, Port Said, Damietta, Kafr El Sheikh, Benha, Shebin El Kom, Minya, Sohag, Qena, Hurghada, 6th of October, and more. You can filter by governorate for easy access.",
        "category": "المدارس",
        "sort_order": 24
    },
    {
        "keywords": "تسجيل طالب, تسجيل ابن, قبول, admission, register student, enroll, registration for child, تقديم طالب, التقديم في المدارس",
        "answer_ar": "للاستفسار عن تسجيل الطلاب والتقديم، يمكنك:\n1) الدخول إلى صفحة المدرسة.\n2) الاطلاع على معلومات الاتصال الخاصة بالمدرسة.\n3) التواصل مباشرة مع إدارة المدرسة.\nالمنصة حالياً لا توفر التقديم الإلكتروني المباشر، ولكننا نعمل على إضافته قريباً.",
        "answer_en": "To inquire about student registration and admission:\n1) Go to the school page.\n2) View the school's contact information.\n3) Contact the school administration directly.\nThe platform currently doesn't offer direct online application, but we are working on adding it soon.",
        "category": "المدارس",
        "sort_order": 25
    },
    {
        "keywords": "رسوم المدارس, مصاريف, تكاليف, school fees, tuition, costs, المصروفات, المصروفات الدراسية, التكلفة",
        "answer_ar": "تختلف المصروفات الدراسية حسب المحافظة ونوع المدرسة والمرحلة الدراسية. يمكنك الاطلاع على معلومات المصروفات في صفحة كل مدرسة ضمن قسم 'المصروفات'. للمزيد من التفاصيل، تواصل مع إدارة المدرسة مباشرة.",
        "answer_en": "Tuition fees vary by governorate, school type, and educational stage. You can view fee information on each school's page under the 'Fees' section. For more details, contact the school administration directly.",
        "category": "المدارس",
        "sort_order": 26
    },
    {
        "keywords": "مدرسة, تسجيل مدرسة, إضافة مدرسة, إدراج مدرسة, add school, register school, list school, تسجيل مدرستك, إضافة مدرستك",
        "answer_ar": "لتسجيل مدرستك في المنصة:\n1) تواصل معنا عبر نموذج الاتصال في الصفحة الرئيسية.\n2) أو اتصل بنا على الرقم 01097000010.\n3) أو راسلنا على البريد الإلكتروني.\nسنقوم بمساعدتك في إنشاء حساب المدرسة واختيار الباقة المناسبة.",
        "answer_en": "To register your school on the platform:\n1) Contact us via the contact form on the homepage.\n2) Or call us at +201097000010.\n3) Or email us.\nWe will help you create a school account and choose the right plan.",
        "category": "المدارس",
        "sort_order": 27
    },
    {
        "keywords": "صور, فيديو, رفع صور, رفع فيديو, media, upload, images, videos, photos, وسائط, تحميل صور, تحميل فيديو",
        "answer_ar": "بعد تسجيل الدخول إلى حساب المدرسة، يمكنك من لوحة التحكم:\n1) الذهاب إلى قسم 'الوسائط'.\n2) رفع الصور والفيديوهات الخاصة بمدرستك.\n3) الحد المسموح يعتمد على باقتك (الباقة البرونزية: صور غير محدودة وفيديو واحد فقط).",
        "answer_en": "After logging into your school account, from the dashboard:\n1) Go to the 'Media' section.\n2) Upload your school's images and videos.\n3) The allowed limit depends on your plan (Bronze: unlimited images and only 1 video).",
        "category": "المدارس",
        "sort_order": 28
    },
    {
        "keywords": "لوحة تحكم المدرسة, school dashboard, school control panel, تحكم المدرسة, لوحة التحكم, الإدارة",
        "answer_ar": "لوحة تحكم المدرسة تمكنك من: إدارة الملف الشخصي للمدرسة، رفع الصور والفيديوهات، إضافة الأنشطة والخدمات، إدارة المعلمين، متابعة الاستخدام والباقة، وعرض الإحصائيات.",
        "answer_en": "The school dashboard allows you to: manage the school profile, upload images and videos, add activities and services, manage teachers, monitor usage and plan, and view statistics.",
        "category": "المدارس",
        "sort_order": 29
    },
    {
        "keywords": "معلم, معلمين, كادر تدريسي, teacher, teachers, staff, المدرسين, أعضاء هيئة التدريس",
        "answer_ar": "يمكن إضافة المعلمين من لوحة تحكم المدرسة. عدد المعلمين المسموح به يعتمد على الباقة: البرونزية (مدرس واحد)، الفضية (3 مدرسين)، الذهبية (غير محدود).",
        "answer_en": "Teachers can be added from the school dashboard. The number of allowed teachers depends on your plan: Bronze (1 teacher), Silver (3 teachers), Gold (unlimited).",
        "category": "المدارس",
        "sort_order": 30
    },
    {
        "keywords": "نشاط, أنشطة مدرسية, خدمات, activities, school activities, services, النشاطات, انشطة",
        "answer_ar": "يمكن إضافة الأنشطة والخدمات المدرسية من لوحة تحكم المدرسة. أضف اسم النشاط، وصف مختصر، وصورة إن وجدت. ستعرض هذه الأنشطة في صفحة المدرسة لأولياء الأمور.",
        "answer_en": "School activities and services can be added from the school dashboard. Add the activity name, brief description, and an image if available. These activities will be displayed on the school page for parents.",
        "category": "المدارس",
        "sort_order": 31
    },
    {
        "keywords": "الملف الشخصي للمدرسة, school profile, صفحة المدرسة, بيانات المدرسة, تعديل بيانات المدرسة",
        "answer_ar": "يمكنك تعديل الملف الشخصي للمدرسة من لوحة التحكم. يشمل الملف: اسم المدرسة، الشعار، صورة الغلاف، المحافظة، العنوان، رقم الهاتف، البريد الإلكتروني، موقع الويب، ووصف المدرسة.",
        "answer_en": "You can edit the school profile from the dashboard. The profile includes: school name, logo, cover image, governorate, address, phone number, email, website, and school description.",
        "category": "المدارس",
        "sort_order": 32
    },
    {
        "keywords": "تقييم المدارس, تقييم, مراجعة, مراجعات, school ratings, reviews, تقييمات, التقييم",
        "answer_ar": "يمكن لأولياء الأمور تقييم المدارس وكتابة مراجعات عنها بعد تسجيل الدخول. التقييمات تساعد أولياء الأمور الآخرين في اختيار المدرسة المناسبة. يتم مراجعة جميع التقييمات قبل النشر.",
        "answer_en": "Parents can rate schools and write reviews after logging in. Ratings help other parents choose the right school. All reviews are reviewed before publication.",
        "category": "المدارس",
        "sort_order": 33
    },
    {
        "keywords": "توثيق المدرسة, التحقق من المدرسة, school verification, verified, موثقة, علامة التوثيق",
        "answer_ar": "المدارس الموثقة (Verified) هي مدارس قامت بتأكيد بياناتها مع إدارة المنصة. تحصل المدارس الموثقة على علامة زرقاء 📘 بجانب اسمها. للتوثيق، تواصل مع فريق الدعم.",
        "answer_en": "Verified schools are those that have confirmed their data with the platform administration. Verified schools receive a blue checkmark 📘 next to their name. To get verified, contact the support team.",
        "category": "المدارس",
        "sort_order": 34
    },
    {
        "keywords": "بيانات الاتصال بالمدرسة, school contact, رقم هاتف المدرسة, عنوان المدرسة, imeil المدرسة, how to contact school",
        "answer_ar": "جميع بيانات الاتصال بالمدرسة متاحة في صفحة المدرسة. تشمل: رقم الهاتف، البريد الإلكتروني، العنوان بالكامل، وموقع الويب إذا وجد. يمكنك التواصل مباشرة مع المدرسة من خلال هذه البيانات.",
        "answer_en": "All school contact information is available on the school page. It includes: phone number, email, full address, and website if available. You can contact the school directly through this information.",
        "category": "المدارس",
        "sort_order": 35
    },
    {
        "keywords": "مواعيد الدراسة, أوقات الدراسة, اليوم الدراسي, school hours, school schedule, timings, دوام المدارس, الحضور والانصراف",
        "answer_ar": "تختلف مواعيد الدراسة من مدرسة لأخرى. عادةً تبدأ الدراسة في المدارس المصرية من الساعة 7:30 صباحاً حتى 2:00 ظهراً تقريباً. يمكنك الاطلاع على المواعيد الدقيقة في صفحة كل مدرسة ضمن قسم 'معلومات المدرسة'.",
        "answer_en": "School hours vary from school to school. Typically, Egyptian schools start from 7:30 AM to around 2:00 PM. You can check the exact times on each school's page under the 'School Information' section.",
        "category": "المدارس",
        "sort_order": 36
    },
    {
        "keywords": "عدد الطلاب, كثافة الفصول, class size, student count, كثافة, أعداد الطلاب, طالب في الفصل",
        "answer_ar": "تختلف كثافة الفصول حسب نوع المدرسة. المدارس الخاصة والدولية عادةً ذات كثافة أقل (20-25 طالباً في الفصل)، بينما المدارس الحكومية قد تصل إلى 40-50 طالباً. يمكنك معرفة متوسط عدد الطلاب في الفصل من صفحة المدرسة.",
        "answer_en": "Class density varies by school type. Private and international schools typically have lower density (20-25 students per class), while government schools may have 40-50 students. You can find the average class size on the school page.",
        "category": "المدارس",
        "sort_order": 37
    },
    {
        "keywords": "الموقع, خريطة, عنوان المدرسة, location, map, school address, العنوان, إحداثيات,导航",
        "answer_ar": "يمكنك عرض موقع المدرسة على الخريطة من صفحة المدرسة. المنصة تدمج مع خرائط جوجل لتسهيل الوصول إلى المدرسة. اضغط على 'عرض على الخريطة' لفتح موقع المدرسة في خرائط جوجل.",
        "answer_en": "You can view the school location on the map from the school page. The platform integrates with Google Maps to make it easy to reach the school. Click 'View on Map' to open the school location in Google Maps.",
        "category": "المدارس",
        "sort_order": 38
    },
    {
        "keywords": "إجازة المدارس, العطلات المدرسية, الإجازات الرسمية, school holidays, official holidays, العطلات, إجازات نصف العام, إجازات نهاية العام",
        "answer_ar": "الإجازات المدرسية في مصر تشمل:\n1) إجازة نصف العام: أسبوعان في يناير/فبراير.\n2) إجازة نهاية العام: تبدأ في يونيو.\n3) الإجازات الرسمية: عيد الفطر، عيد الأضحى، 6 أكتوبر، 25 يناير، عيد العمال، شم النسيم.\nيمكنك الاطلاع على تقويم الإجازات في صفحة المدرسة.",
        "answer_en": "School holidays in Egypt include:\n1) Mid-year break: two weeks in January/February.\n2) End-of-year break: starts in June.\n3) Public holidays: Eid al-Fitr, Eid al-Adha, October 6, January 25, Labor Day, Sham El Nessim.\nYou can check the holiday calendar on the school page.",
        "category": "المدارس",
        "sort_order": 39
    },

    # ═══════════════════════════════════════════
    # أولياء الأمور (Parents)
    # ═══════════════════════════════════════════
    {
        "keywords": "ولي أمر, أولياء الأمور, parent, parents, guardian, ولي أمر الطالب, اب, ام",
        "answer_ar": "كولي أمر، يمكنك من خلال المنصة: البحث عن المدارس المناسبة لأبنائك، مقارنة المدارس بجانب بعض، مشاهدة الصور والفيديوهات الحقيقية، الاطلاع على أنشطة المدرسة وخدماتها، التواصل مع إدارة المدرسة، وحفظ المدارس المفضلة.",
        "answer_en": "As a parent, through the platform you can: search for suitable schools for your children, compare schools side by side, view real photos and videos, browse school activities and services, contact school administration, and save favorite schools.",
        "category": "أولياء الأمور",
        "sort_order": 40
    },
    {
        "keywords": "المدارس المفضلة, حفظ المدارس, مفضلة, favorites, save schools, wishlist, المفضلة, حفظ المفضلة",
        "answer_ar": "يمكنك إضافة المدارس إلى المفضلة للرجوع إليها لاحقاً. اضغط على أيقونة القلب 💙 في صفحة المدرسة أو في نتائج البحث. يمكنك الوصول إلى قائمة المفضلة من صفحة 'المفضلة' في حسابك.",
        "answer_en": "You can add schools to your favorites for later reference. Click the heart icon 💙 on the school page or in search results. You can access your favorites list from the 'Favorites' page in your account.",
        "category": "أولياء الأمور",
        "sort_order": 41
    },
    {
        "keywords": "مقارنة المدارس, مقارنة, compare, comparison, قارن, المقارنة بين المدارس, أيهما أفضل",
        "answer_ar": "يمكنك مقارنة المدارس بجانب بعضها البعض. اختر المدارس التي تريد مقارنتها ثم اضغط على 'مقارنة'. ستظهر لك المعلومات جنباً إلى جنب لتسهيل اتخاذ القرار المناسب.",
        "answer_en": "You can compare schools side by side. Select the schools you want to compare and click 'Compare'. Information will appear side by side to help you make the right decision.",
        "category": "أولياء الأمور",
        "sort_order": 42
    },
    {
        "keywords": "إشعارات أولياء الأمور, تنبيهات, notifications, alerts, إشعارات, التنبيهات, اخبار المدارس",
        "answer_ar": "ستصلك إشعارات عند إضافة مدارس جديدة في منطقتك، أو عند تحديث بيانات مدرسة من مفضلتك، أو عند وجود عروض وباقات جديدة. يمكنك التحكم في الإشعارات من صفحة الإعدادات.",
        "answer_en": "You will receive notifications when new schools are added in your area, when a school in your favorites updates its data, or when there are new offers and plans. You can control notifications from the Settings page.",
        "category": "أولياء الأمور",
        "sort_order": 43
    },
    {
        "keywords": "إدارة حساب ولي الأمر, parent account management, تغيير بيانات ولي الأمر, ضبط الحساب",
        "answer_ar": "يمكنك إدارة حسابك كولي أمر من لوحة التحكم الخاصة بك. تشمل الإعدادات: تحديث البيانات الشخصية، تغيير كلمة المرور، إدارة الإشعارات، وعرض المدارس المفضلة.",
        "answer_en": "You can manage your parent account from your dashboard. Settings include: updating personal information, changing password, managing notifications, and viewing favorite schools.",
        "category": "أولياء الأمور",
        "sort_order": 44
    },

    # ═══════════════════════════════════════════
    # المناهج (Curricula)
    # ═══════════════════════════════════════════
    {
        "keywords": "المناهج, المناهج الدراسية, curricula, curriculum, المنهج, النظام التعليمي, educational system, المناهج المتاحة",
        "answer_ar": "تغطي المنصة المدارس التي تقدم مناهج متنوعة:\n1) المنهج المصري (وزارة التربية والتعليم).\n2) المنهج البريطاني (IGCSE).\n3) المنهج الأمريكي (American Diploma).\n4) المنهج الفرنسي.\n5) المنهج الألماني (اللغة الألمانية).\nيمكنك تصفية البحث حسب المنهج الدراسي.",
        "answer_en": "The platform covers schools offering various curricula:\n1) Egyptian curriculum (Ministry of Education).\n2) British curriculum (IGCSE).\n3) American curriculum (American Diploma).\n4) French curriculum.\n5) German curriculum.\nYou can filter search by curriculum.",
        "category": "المناهج",
        "sort_order": 45
    },
    {
        "keywords": "المنهج المصري, منهج مصري, وزارة التربية والتعليم, egyptian curriculum, ministry of education, المنهج الحكومي",
        "answer_ar": "المنهج المصري هو المنهج الرسمي لوزارة التربية والتعليم في مصر. يشمل جميع المراحل من رياض الأطفال حتى الثانوية العامة. يتم تدريسه في المدارس الحكومية والخاصة والتجريبية.",
        "answer_en": "The Egyptian curriculum is the official curriculum of the Ministry of Education in Egypt. It covers all stages from kindergarten to Thanaweya Amma. It is taught in government, private, and experimental schools.",
        "category": "المناهج",
        "sort_order": 46
    },
    {
        "keywords": "منهج بريطاني, igcse, بريطاني, british curriculum, cambridge, edexcel, البريطاني, IGCSE, GCSE",
        "answer_ar": "المنهج البريطاني (IGCSE) هو منهج دولي معترف به، ويدرس باللغة الإنجليزية. يشمل عدة مراحل: المرحلة التأسيسية، المرحلة الابتدائية، المرحلة الإعدادية، ثم شهادة IGCSE في سن 16 عاماً. تقدمه المدارس الدولية في مصر.",
        "answer_en": "The British curriculum (IGCSE) is an internationally recognized curriculum taught in English. It includes: Foundation stage, Primary, Secondary, then the IGCSE certificate at age 16. Offered by international schools in Egypt.",
        "category": "المناهج",
        "sort_order": 47
    },
    {
        "keywords": "منهج أمريكي, american diploma, أمريكي, american curriculum, sat, american high school, SAT",
        "answer_ar": "المنهج الأمريكي (American Diploma) هو منهج دولي يُدرس باللغة الإنجليزية. يشمل المراحل من KG حتى Grade 12. يمنح الطالب شهادة الثانوية الأمريكية التي تمكنه من الالتحاق بالجامعات المصرية والدولية بعد اجتياز اختبار SAT.",
        "answer_en": "The American curriculum (American Diploma) is an international curriculum taught in English. It includes stages from KG to Grade 12. It grants the American High School Diploma, enabling students to enter Egyptian and international universities after passing the SAT.",
        "category": "المناهج",
        "sort_order": 48
    },
    {
        "keywords": "منهج فرنسي, فرنسي, french curriculum, الفرنسي, باكالوريا فرنسية, baccalaureate, French baccalaureate",
        "answer_ar": "المنهج الفرنسي يُدرس باللغة الفرنسية ويتبع نظام التعليم الفرنسي. يمنح الطالب شهادة البكالوريا الفرنسية (Baccalaureate) التي تؤهل للالتحاق بالجامعات المصرية والفرنسية والدولية.",
        "answer_en": "The French curriculum is taught in French and follows the French education system. It grants the French Baccalaureate certificate, qualifying students for Egyptian, French, and international universities.",
        "category": "المناهج",
        "sort_order": 49
    },
    {
        "keywords": "منهج ألماني, ألماني, german curriculum, german, deutsche schule, الألماني, اللغة الألمانية, abitur",
        "answer_ar": "المنهج الألماني يُدرس باللغة الألمانية ويمنح شهادة الثانوية الألمانية (Abitur) أو شهادة اللغة الألمانية (DSD). توجد هذه المدارس في القاهرة والإسكندرية والغردقة.",
        "answer_en": "The German curriculum is taught in German and grants the German Abitur certificate or the German Language Diploma (DSD). These schools are located in Cairo, Alexandria, and Hurghada.",
        "category": "المناهج",
        "sort_order": 50
    },
    {
        "keywords": "اختيار المنهج, اختيار المنهج المناسب, كيفية اختيار المدرسة, choose curriculum, how to choose school, إيه المنهج المناسب, نصائح اختيار المدرسة",
        "answer_ar": "عند اختيار المنهج المناسب لابنك، ضع في اعتبارك:\n1) قدرات وميول الطالب اللغوية والأكاديمية.\n2) ميزانية الأسرة والمصروفات الدراسية.\n3) الجامعة التي يرغب الطالب في الالتحاق بها مستقبلاً.\n4) قرب المدرسة من مكان السكن.\n5) سمعة المدرسة وتقييمات أولياء الأمور.\nيمكنك استخدام المنصة لمقارنة المدارس والمناهج بسهولة.",
        "answer_en": "When choosing the right curriculum for your child, consider:\n1) The student's linguistic and academic abilities and interests.\n2) The family budget and tuition fees.\n3) The university the student wishes to attend in the future.\n4) Proximity of the school to home.\n5) School reputation and parent reviews.\nYou can use the platform to easily compare schools and curricula.",
        "category": "المناهج",
        "sort_order": 51
    },
    {
        "keywords": "المنهج السعودي, منهج سعودي, saudi curriculum, مدارس سعودية في مصر",
        "answer_ar": "توجد بعض المدارس السعودية في مصر التي تتبع المنهج السعودي، وتقع بشكل أساسي في القاهرة. يمكنك البحث عنها باستخدام فلتر 'السعودي' في قسم المناهج على المنصة.",
        "answer_en": "There are some Saudi schools in Egypt that follow the Saudi curriculum, mainly located in Cairo. You can search for them using the 'Saudi' filter in the curricula section on the platform.",
        "category": "المناهج",
        "sort_order": 52
    },

    # ═══════════════════════════════════════════
    # التقديم (Admission)
    # ═══════════════════════════════════════════
    {
        "keywords": "مواعيد التقديم, التقديم للمدارس, application dates, admission dates, التقديم, وقت التقديم, امتى التقديم, بدأ التقديم",
        "answer_ar": "مواعيد التقديم للمدارس في مصر تختلف حسب نوع المدرسة:\n1) المدارس الحكومية: يبدأ التقديم عادة في مايو/يونيو من كل عام.\n2) المدارس الخاصة والدولية: تبدأ من يناير حتى سبتمبر.\n3) المدارس التجريبية: من مايو إلى يوليو.\nيُرجى متابعة إعلانات كل مدرسة للحصول على المواعيد الدقيقة.",
        "answer_en": "School application dates in Egypt vary by school type:\n1) Government schools: usually start in May/June each year.\n2) Private and international schools: from January to September.\n3) Experimental schools: from May to July.\nPlease follow each school's announcements for exact dates.",
        "category": "التقديم",
        "sort_order": 53
    },
    {
        "keywords": "الأوراق المطلوبة, المستندات المطلوبة, required documents, documents for school, ورق التقديم, أوراق التقديم, ملف التقديم",
        "answer_ar": "الأوراق المطلوبة عادة للتقديم في المدارس:\n1) شهادة ميلاد الطالب (كمبيوتر).\n2) صورة من بطاقة ولي الأمر.\n3) عدد 4-6 صور شخصية حديثة للطالب.\n4) شهادة صحية (توقيع الكشف الطبي).\n5) شهادة من المدرسة السابقة (للتحويل).\n6) ملف التقديم (ملف حفظ الملفات).\n7) طلب الالتحاق معبأ.\nقد تختلف الأوراق من مدرسة لأخرى.",
        "answer_en": "Documents typically required for school admission:\n1) Student's birth certificate (computerized).\n2) Copy of parent's ID.\n3) 4-6 recent personal photos of the student.\n4) Health certificate (medical examination).\n5) Certificate from previous school (for transfer).\n6) Application file (file folder).\n7) Completed admission application form.\nDocuments may vary from school to school.",
        "category": "التقديم",
        "sort_order": 54
    },
    {
        "keywords": "اختبارات القبول, امتحانات القبول, entrance exams, admission tests, اختبارات, امتحانات, التقييم, اختبار القبول",
        "answer_ar": "تختلف اختبارات القبول حسب المدرسة والمرحلة:\n1) رياض الأطفال: مقابلة شخصية وتقييم مهارات بسيط.\n2) المرحلة الابتدائية: اختبار في اللغة العربية والرياضيات واللغة الإنجليزية.\n3) المرحلة الإعدادية والثانوية: اختبارات في المواد الأساسية.\n4) المدارس الدولية: اختبار باللغة الإنجليزية وقد يشمل اختبار CAT4 أو IQ.",
        "answer_en": "Admission tests vary by school and stage:\n1) Kindergarten: personal interview and simple skills assessment.\n2) Primary stage: test in Arabic, Mathematics, and English.\n3) Preparatory and secondary stages: tests in core subjects.\n4) International schools: English test may include CAT4 or IQ test.",
        "category": "التقديم",
        "sort_order": 55
    },
    {
        "keywords": "المقابلات الشخصية, مقابلة القبول, مقابلة الطالب, interviews, personal interview, admission interview, مقابلة, إنترفيو",
        "answer_ar": "المقابلات الشخصية جزء مهم من عملية القبول في معظم المدارس. عادةً تشمل:\n1) مقابلة مع الطالب لتقييم مهاراته.\n2) مقابلة مع ولي الأمر.\n3) قد تشمل تقييماً نفسياً وتربوياً.\nتتواصل المدرسة مع أولياء الأمور لتحديد موعد المقابلة بعد تقديم الطلب.",
        "answer_en": "Personal interviews are an important part of the admission process in most schools. They usually include:\n1) An interview with the student to assess skills.\n2) An interview with the parent.\n3) May include psychological and educational assessment.\nThe school contacts parents to schedule the interview after application submission.",
        "category": "التقديم",
        "sort_order": 56
    },
    {
        "keywords": "السن المطلوب, سن القبول, السن القانوني, age requirement, admission age, age for school, السن, السن المناسب",
        "answer_ar": "السن القانوني للقبول في المدارس المصرية:\n1) رياض الأطفال (KG1): 4 سنوات.\n2) رياض الأطفال (KG2): 5 سنوات.\n3) الصف الأول الابتدائي: 6 سنوات.\n4) الصف الأول الإعدادي: 12 سنة.\n5) الصف الأول الثانوي: 15 سنة.\nيسمح بفارق 6 أشهر فقط عن السن المحدد.",
        "answer_en": "Legal age for admission in Egyptian schools:\n1) Kindergarten (KG1): 4 years.\n2) Kindergarten (KG2): 5 years.\n3) Grade 1 Primary: 6 years.\n4) Grade 1 Preparatory: 12 years.\n5) Grade 1 Secondary: 15 years.\nOnly a 6-month difference from the specified age is allowed.",
        "category": "التقديم",
        "sort_order": 57
    },
    {
        "keywords": "تحويل الطلاب, نقل الطالب, تحويل من مدرسة لأخرى, student transfer, transfer student, نقل قيد, التحويل بين المدارس",
        "answer_ar": "لتحويل الطالب من مدرسة إلى أخرى:\n1) الحصول على شهادة من المدرسة السابقة (بيان نجاح وسلوك).\n2) التقدم إلى المدرسة الجديدة مع الأوراق المطلوبة.\n3) إحضار ملف الطالب من المدرسة القديمة.\n4) سداد الرسوم المقررة.\nيمكن إجراء التحويل خلال العام الدراسي أو في بدايته.",
        "answer_en": "To transfer a student from one school to another:\n1) Obtain a certificate from the previous school (academic and behavior record).\n2) Apply to the new school with required documents.\n3) Bring the student's file from the old school.\n4) Pay applicable fees.\nTransfer can be done during the academic year or at the beginning.",
        "category": "التقديم",
        "sort_order": 58
    },
    {
        "keywords": "الأولوية في القبول, priority admission, أسبقية القبول, معايير القبول, قبول الأولوية, أخوة, أشقاء",
        "answer_ar": "أولوية القبول في المدارس تكون عادةً:\n1) لإخوة الطلاب المسجلين بالفعل.\n2) لأبناء العاملين بالمدرسة.\n3) حسب تاريخ تقديم الطلب (الأسبقية).\n4) أبناء الخريجين (في بعض المدارس).\nقد تختلف معايير الأولوية من مدرسة لأخرى.",
        "answer_en": "Admission priority in schools is usually:\n1) For siblings of currently enrolled students.\n2) For children of school employees.\n3) Based on application date (first come, first served).\n4) Children of alumni (in some schools).\nPriority criteria may vary from school to school.",
        "category": "التقديم",
        "sort_order": 59
    },

    # ═══════════════════════════════════════════
    # المراحل التعليمية (Educational Stages)
    # ═══════════════════════════════════════════
    {
        "keywords": "المراحل التعليمية, مراحل التعليم, stages, educational stages, المراحل الدراسية, مراحل التعليم في مصر",
        "answer_ar": "المراحل التعليمية في مصر:\n1) رياض الأطفال (KG1-KG2): سن 4-6 سنوات.\n2) المرحلة الابتدائية: الصف الأول حتى السادس (6 سنوات).\n3) المرحلة الإعدادية: الصف الأول حتى الثالث (3 سنوات).\n4) المرحلة الثانوية: الصف الأول حتى الثالث (3 سنوات).\nكل مرحلة تؤهل للانتقال إلى المرحلة التي تليها.",
        "answer_en": "Educational stages in Egypt:\n1) Kindergarten (KG1-KG2): ages 4-6.\n2) Primary stage: Grade 1 to 6 (6 years).\n3) Preparatory stage: Grade 1 to 3 (3 years).\n4) Secondary stage: Grade 1 to 3 (3 years).\nEach stage qualifies for progression to the next.",
        "category": "المراحل التعليمية",
        "sort_order": 60
    },
    {
        "keywords": "رياض أطفال, حضانات, kg, kindergarten, nursery, kg1, kg2, pre school, تمهيدي, الحضانة, الروضة",
        "answer_ar": "رياض الأطفال (KG) هي مرحلة ما قبل المدرسة الابتدائية وتشمل:\n1) KG1: للأطفال من 4-5 سنوات.\n2) KG2: للأطفال من 5-6 سنوات.\nتهدف إلى إعداد الطفل للمرحلة الابتدائية من خلال الأنشطة التفاعلية واللعب التعليمي.",
        "answer_en": "Kindergarten (KG) is the pre-primary stage and includes:\n1) KG1: for children aged 4-5.\n2) KG2: for children aged 5-6.\nIt aims to prepare children for primary school through interactive activities and educational play.",
        "category": "المراحل التعليمية",
        "sort_order": 61
    },
    {
        "keywords": "المرحلة الابتدائية, ابتدائي, primary school, elementary, الصفوف الابتدائية, الابتدائي",
        "answer_ar": "المرحلة الابتدائية تمتد من الصف الأول حتى السادس (6 سنوات). يدرس الطالب المواد الأساسية: اللغة العربية، اللغة الإنجليزية، الرياضيات، العلوم، الدراسات الاجتماعية، والتربية الدينية.",
        "answer_en": "The primary stage extends from Grade 1 to 6 (6 years). The student studies core subjects: Arabic, English, Mathematics, Science, Social Studies, and Religious Education.",
        "category": "المراحل التعليمية",
        "sort_order": 62
    },
    {
        "keywords": "المرحلة الإعدادية, إعدادي, preparatory school, middle school, الإعدادي, الصفوف الإعدادية",
        "answer_ar": "المرحلة الإعدادية تمتد من الصف الأول حتى الثالث (3 سنوات). يدرس الطالب مواد أكثر تخصصاً تشمل: اللغة العربية، اللغات الأجنبية، الرياضيات، العلوم (فيزياء، كيمياء، أحياء)، الدراسات الاجتماعية، والتربية الدينية.",
        "answer_en": "The preparatory stage extends from Grade 1 to 3 (3 years). Students study more specialized subjects including: Arabic, foreign languages, Mathematics, Science (Physics, Chemistry, Biology), Social Studies, and Religious Education.",
        "category": "المراحل التعليمية",
        "sort_order": 63
    },
    {
        "keywords": "المرحلة الثانوية, ثانوي, secondary school, high school, الثانوي, الثانوية, ثانوية عامة",
        "answer_ar": "المرحلة الثانوية تمتد من الصف الأول حتى الثالث (3 سنوات). تنقسم إلى:\n1) الثانوية العامة: بعد الصف الثاني يختار الطالب (علمي علوم، علمي رياضة، أدبي).\n2) الثانوية الفنية: صناعي، زراعي، تجاري، فندقي.\nالثانوية العامة تؤهل للالتحاق بالجامعات المصرية.",
        "answer_en": "The secondary stage extends from Grade 1 to 3 (3 years). It is divided into:\n1) General Secondary: after Grade 2, students choose (Science, Mathematics, Literary).\n2) Technical Secondary: Industrial, Agricultural, Commercial, Hotel.\nGeneral Secondary qualifies for enrollment in Egyptian universities.",
        "category": "المراحل التعليمية",
        "sort_order": 64
    },
    {
        "keywords": "التعليم الفني, مدارس فنية, technical education, vocational, صناعي, زراعي, تجاري, فندقي, التعليم المهني",
        "answer_ar": "التعليم الفني في مصر يشمل:\n1) التعليم الصناعي: تخصصات ميكانيكا، كهرباء، إلكترونيات، عمارة.\n2) التعليم الزراعي.\n3) التعليم التجاري.\n4) التعليم الفندقي.\n5) مدارس التعليم الفني المتطور (STEM).\nيمنح التعليم الفني شهادة تؤهل لسوق العمل أو استكمال التعليم الجامعي.",
        "answer_en": "Technical education in Egypt includes:\n1) Industrial education: Mechanics, Electricity, Electronics, Architecture.\n2) Agricultural education.\n3) Commercial education.\n4) Hotel education.\n5) Advanced technical schools.\nTechnical education grants a certificate qualifying for the job market or continuing university education.",
        "category": "المراحل التعليمية",
        "sort_order": 65
    },

    # ═══════════════════════════════════════════
    # تقني (Technical)
    # ═══════════════════════════════════════════
    {
        "keywords": "مشكلة تقنية, مشكلة, خطأ, bug, error, technical issue, problem, not working, مشاكل, عطل, في مشكلة, بايظ",
        "answer_ar": "إذا واجهتك أي مشكلة تقنية، يرجى المحاولة أولاً بـ:\n1) تحديث الصفحة (F5).\n2) مسح كاش المتصفح (Cache).\n3) تجربة متصفح آخر.\nإذا استمرت المشكلة، تواصل معنا عبر الهاتف 01097000010 أو عبر نموذج الاتصال مع توضيح المشكلة بالتفصيل.",
        "answer_en": "If you encounter any technical issue, please first try:\n1) Refreshing the page (F5).\n2) Clearing your browser cache.\n3) Trying another browser.\nIf the problem persists, contact us at +201097000010 or via the contact form with a detailed description.",
        "category": "تقني",
        "sort_order": 66
    },
    {
        "keywords": "تطبيق جوال, تطبيق, mobile app, app, ios, android, iphone, جوال, موبايل, آب ستور, جوجل بلاي",
        "answer_ar": "حالياً المنصة متاحة عبر المتصفح (Web App) وهي متوافقة تماماً مع الجوال. نحن نعمل على تطوير تطبيقات الجوال لأنظمة iOS و Android وسيتم إطلاقها قريباً بإذن الله.",
        "answer_en": "Currently the platform is available as a web app and is fully mobile-compatible. We are developing mobile applications for iOS and Android which will be launched soon, God willing.",
        "category": "تقني",
        "sort_order": 67
    },
    {
        "keywords": "اللغة, تغيير اللغة, English, العربية, language, change language, switch language, English language, لغة انجليزية, عربي",
        "answer_ar": "يمكنك تغيير لغة المنصة بالضغط على أيقونة اللغة 🌐 في أعلى الصفحة. المنصة تدعم اللغتين العربية والإنجليزية بشكل كامل. يمكنك التبديل بينهما في أي وقت.",
        "answer_en": "You can change the platform language by clicking the language icon 🌐 at the top of the page. The platform fully supports both Arabic and English. You can switch between them at any time.",
        "category": "تقني",
        "sort_order": 68
    },
    {
        "keywords": "المتصفح, توافق المتصفحات, browser compatibility, chrome, firefox, edge, safari, متصفح, متصفحات, جوجل كروم",
        "answer_ar": "المنصة متوافقة مع جميع المتصفحات الحديثة:\n✅ Google Chrome (أفضل أداء)\n✅ Mozilla Firefox\n✅ Microsoft Edge\n✅ Safari\nيرجى التأكد من تحديث متصفحك لأحدث إصدار للحصول على أفضل تجربة.",
        "answer_en": "The platform is compatible with all modern browsers:\n✅ Google Chrome (best performance)\n✅ Mozilla Firefox\n✅ Microsoft Edge\n✅ Safari\nPlease make sure your browser is updated to the latest version for the best experience.",
        "category": "تقني",
        "sort_order": 69
    },
    {
        "keywords": "الأمان والخصوصية, أمان, خصوصية, بيانات, security, privacy, data protection, حماية البيانات, خصوصية البيانات, آمن",
        "answer_ar": "نحن نأخذ أمان وخصوصية بياناتك على محمل الجد:\n1) جميع البيانات مشفرة باستخدام SSL.\n2) كلمات المرور مشفرة ولا يمكن لأحد الاطلاع عليها.\n3) لا نشارك بيانات المستخدمين مع أطراف ثالثة.\n4) يمكنك طلب حذف بياناتك في أي وقت.\nللمزيد، راجع سياسة الخصوصية في أسفل الصفحة.",
        "answer_en": "We take your data security and privacy very seriously:\n1) All data is encrypted using SSL.\n2) Passwords are encrypted and cannot be viewed by anyone.\n3) We do not share user data with third parties.\n4) You can request deletion of your data at any time.\nFor more, see the Privacy Policy at the bottom of the page.",
        "category": "تقني",
        "sort_order": 70
    },

    # ═══════════════════════════════════════════
    # الدعم (Support)
    # ═══════════════════════════════════════════
    {
        "keywords": "اتصال, تواصل, دعم, contact, support, help, customer service, اتصل بنا, تواصل معنا, خدمة العملاء, كستمر سيرفس",
        "answer_ar": "يمكنك التواصل معنا عبر:\n📞 الهاتف: 01097000010\n📧 البريد الإلكتروني: support@treeda-expo.com\n💬 واتساب: +201097000010\n📍 العنوان: القاهرة، جمهورية مصر العربية\n🌐 الموقع: www.treeda-expo.com",
        "answer_en": "You can contact us via:\n📞 Phone: +201097000010\n📧 Email: support@treeda-expo.com\n💬 WhatsApp: +201097000010\n📍 Address: Cairo, Egypt\n🌐 Website: www.treeda-expo.com",
        "category": "الدعم",
        "sort_order": 71
    },
    {
        "keywords": "شكوى, اقتراح, complaint, suggestion, feedback, شاكي, عايز أشتكي, عندي اقتراح, اقتراحات, شكاوى",
        "answer_ar": "نرحب باقتراحاتك وشكواك. يمكنك مراسلتنا عبر نموذج الاتصال في الموقع أو عبر البريد الإلكتروني support@treeda-expo.com. يتم الرد على جميع الاستفسارات خلال 24 ساعة.",
        "answer_en": "We welcome your suggestions and complaints. You can contact us via the contact form on the website or via email at support@treeda-expo.com. All inquiries are answered within 24 hours.",
        "category": "الدعم",
        "sort_order": 72
    },
    {
        "keywords": "أوقات العمل, ساعات العمل, working hours, business hours, الدوام, مواعيد العمل, أوقات الدعم",
        "answer_ar": "نحن متاحون من الأحد إلى الخميس، من 9 صباحاً حتى 9 مساءً بتوقيت مصر. الجمعة والسبت إجازة رسمية. يمكنك ترك رسالة في أي وقت وسنرد عليك في أول يوم عمل.",
        "answer_en": "We are available Sunday to Thursday, from 9 AM to 9 PM Egypt time. Friday and Saturday are official holidays. You can leave a message anytime and we will reply on the first working day.",
        "category": "الدعم",
        "sort_order": 73
    },
    {
        "keywords": "شات مباشر, محادثة مباشرة, live chat, محادثة فورية, شات, تكلم مع موظف, تحدث مع الدعم",
        "answer_ar": "خدمة المحادثة المباشرة (Live Chat) متاحة خلال ساعات العمل الرسمية. اضغط على أيقونة الشات في الزاوية السفلية لبدء محادثة مع فريق الدعم. خارج أوقات العمل، يمكنك استخدام المساعد الذكي أو ترك رسالة.",
        "answer_en": "Live chat is available during official working hours. Click the chat icon in the bottom corner to start a conversation with the support team. Outside working hours, you can use the AI assistant or leave a message.",
        "category": "الدعم",
        "sort_order": 74
    },
    {
        "keywords": "وسائل التواصل الاجتماعي, فيسبوك, تويتر, انستغرام, social media, facebook, twitter, instagram, linkedin, لينكد إن, يوتيوب, youtube, صفحتنا",
        "answer_ar": "تابعنا على وسائل التواصل الاجتماعي:\n📘 فيسبوك: TreedaExpo\n📸 انستغرام: @treeda_expo\n🐦 تويتر: @TreedaExpo\n▶️ يوتيوب: Treeda Expo\n💼 لينكد إن: Treeda Expo\nننشر عروضاً حصرية وأخبار التعليم في مصر.",
        "answer_en": "Follow us on social media:\n📘 Facebook: TreedaExpo\n📸 Instagram: @treeda_expo\n🐦 Twitter: @TreedaExpo\n▶️ YouTube: Treeda Expo\n💼 LinkedIn: Treeda Expo\nWe share exclusive offers and education news in Egypt.",
        "category": "الدعم",
        "sort_order": 75
    },

    # ═══════════════════════════════════════════
    # مصر (Egypt-Specific Topics)
    # ═══════════════════════════════════════════
    {
        "keywords": "المدارس التجريبية, تجريبية, experimental schools, مدارس تجريبية, المدارس التجريبية في مصر, تجريبي لغات, تجريبي عربي",
        "answer_ar": "المدارس التجريبية هي مدارس حكومية متميزة تدرس المنهج المصري ولكن باهتمام أكبر باللغات الأجنبية. أنواعها:\n1) تجريبية (عربي): تدريس بالعربية مع لغة أجنبية.\n2) تجريبية (لغات): تدريس بالإنجليزية للمواد العلمية.\nتتميز بمصروفات أقل من المدارس الخاصة وجودة تعليم عالية.",
        "answer_en": "Experimental schools are distinguished government schools that teach the Egyptian curriculum with greater emphasis on foreign languages. Types:\n1) Experimental (Arabic): taught in Arabic with a foreign language.\n2) Experimental (Languages): taught in English for scientific subjects.\nThey feature lower fees than private schools with high educational quality.",
        "category": "مصر",
        "sort_order": 76
    },
    {
        "keywords": "المدارس الرسمية للغات, رسمية لغات, official language schools, مدارس رسمية للغات, الرسمية للغات",
        "answer_ar": "المدارس الرسمية للغات هي مدارس حكومية تدرس المنهج المصري باللغة الإنجليزية. تم استحداثها لتكون بديلاً للمدارس التجريبية. تتميز بمصروفات دراسية منخفضة نسبياً وجودة تعليم جيدة.",
        "answer_en": "Official Language Schools are government schools that teach the Egyptian curriculum in English. They were established as an alternative to experimental schools. They feature relatively low tuition fees and good educational quality.",
        "category": "مصر",
        "sort_order": 77
    },
    {
        "keywords": "نظام التعليم الجديد, نظام 2.0, التعليم الجديد في مصر, new education system, education 2.0, نظام التعليم المصري الجديد, تطوير التعليم",
        "answer_ar": "نظام التعليم الجديد (Education 2.0) أطلقته وزارة التربية والتعليم في مصر عام 2018. يشمل:\n1) نظام التقييم الجديد (امتحانات متعددة بدلاً من امتحان واحد).\n2) مناهج مطورة تركز على الفهم وليس الحفظ.\n3) إدخال التكنولوجيا في التعليم.\n4) إلغاء امتحانات الثانوية العامة التقليدية تدريجياً (تم تعديله).\n5) نظام الثانوية التراكمية (المجموع التراكمي).",
        "answer_en": "The new education system (Education 2.0) was launched by the Egyptian Ministry of Education in 2018. It includes:\n1) New assessment system (multiple exams instead of one final exam).\n2) Developed curricula focusing on understanding, not memorization.\n3) Introducing technology in education.\n4) Gradually phasing out traditional Thanaweya Amma exams (subsequently modified).\n5) Cumulative grading system for secondary school.",
        "category": "مصر",
        "sort_order": 78
    },
    {
        "keywords": "التابلت المدرسي, تابلت, tablet, school tablet, تابلت التعليم, تابلت الثانوية, التابلت",
        "answer_ar": "التابلت المدرسي هو جهاز لوحي يتم توزيعه على طلاب المرحلة الثانوية في مصر ضمن نظام التعليم الجديد. يحتوي على:\n1) المناهج الدراسية إلكترونياً.\n2) بنك المعرفة المصري.\n3) منصات التعلم التفاعلية.\nالتابلت ملك للطالب بعد التخرج أو يتم تسليمه حسب سياسة كل مدرسة.",
        "answer_en": "The school tablet is a tablet device distributed to secondary school students in Egypt as part of the new education system. It contains:\n1) Electronic curricula.\n2) Egyptian Knowledge Bank.\n3) Interactive learning platforms.\nThe tablet becomes the student's property after graduation or is returned depending on school policy.",
        "category": "مصر",
        "sort_order": 79
    },
    {
        "keywords": "الثانوية العامة, ثانوية عامة, thanaweya amma, general secondary, تنسيق الجامعات, مجموع الثانوية, التنسيق, نتيجة الثانوية",
        "answer_ar": "الثانوية العامة هي شهادة إتمام المرحلة الثانوية في مصر. نظامها:\n1) يدرس الطالب 3 سنوات (الصفوف الأول والثاني والثالث الثانوي).\n2) في الصف الثالث، يؤدي امتحانات نهائية في المواد المقررة.\n3) المجموع الكلي يحدد تنسيق الجامعة.\n4) الشعبتان: علمي (علوم/رياضة) وأدبي.\nهي الشهادة الرئيسية للالتحاق بالجامعات المصرية.",
        "answer_en": "Thanaweya Amma is the General Secondary School Certificate in Egypt. Its system:\n1) Students study for 3 years (Grades 1, 2, and 3 secondary).\n2) In Grade 3, final exams are taken in prescribed subjects.\n3) The total score determines university admission (coordination).\n4) Two tracks: Scientific (Sciences/Mathematics) and Literary.\nIt is the main certificate for enrollment in Egyptian universities.",
        "category": "مصر",
        "sort_order": 80
    },
    {
        "keywords": "مجموعات التقوية, دروس خصوصية, tutoring, private lessons, دروس, تقوية, مذكرات, سنتر, سناتر, خصوصي",
        "answer_ar": "مجموعات التقوية والدروس الخصوصية شائعة في مصر لدعم العملية التعليمية. يمكنك:\n1) البحث عن مدرسين متخصصين عبر المنصة.\n2) الاستفسار من المدرسة عن مجموعات التقوية المتاحة.\n3) التواصل مع معلمين متخصصين للمراجعات والامتحانات.\nننصح دائماً بالاعتماد على المدرسة أولاً ثم مجموعات التقوية كمكمل.",
        "answer_en": "Tutoring groups and private lessons are common in Egypt to support education. You can:\n1) Search for specialized teachers through the platform.\n2) Inquire at the school about available tutoring groups.\n3) Contact specialized teachers for reviews and exams.\nWe always recommend relying on school first, then tutoring as a supplement.",
        "category": "مصر",
        "sort_order": 81
    },
    {
        "keywords": "الدمج التعليمي, دمج, inclusive education, special needs, ذوي احتياجات خاصة, تعليم مدمج, الدمج, صعوبات تعلم, التربية الخاصة",
        "answer_ar": "الدمج التعليمي هو إدماج الطلاب ذوي الاحتياجات الخاصة في المدارس العادية. في مصر:\n1) توجد فصول دمج في العديد من المدارس الحكومية والخاصة.\n2) يتم تقديم الدعم المناسب حسب احتياجات كل طالب.\n3) يوجد نظام تعليمي متكامل لذوي الاحتياجات البصرية والسمعية والحركية.\n4) بعض المدارس متخصصة بالكامل في التربية الخاصة.\nيمكنك تصفية البحث لاختيار المدارس التي تخدم احتياجات ابنك.",
        "answer_en": "Inclusive education integrates students with special needs into regular schools. In Egypt:\n1) Inclusion classes exist in many government and private schools.\n2) Appropriate support is provided based on each student's needs.\n3) There is an integrated educational system for visually, hearing, and physically impaired students.\n4) Some schools are fully specialized in special education.\nYou can filter search to find schools that serve your child's needs.",
        "category": "مصر",
        "sort_order": 82
    },
    {
        "keywords": "مدارس المتفوقين, stem, مدارس stem, مدارس العلوم والتكنولوجيا, stem schools, مدارس المتفوقين في مصر, مدارس النيل, النيل",
        "answer_ar": "مدارس المتفوقين (STEM) هي مدارس حكومية متميزة للطلاب المتفوقين في العلوم والتكنولوجيا والهندسة والرياضيات. شروط الالتحاق:\n1) الحصول على مجموع مرتفع في الشهادة الإعدادية.\n2) اجتياز اختبارات القبول.\n3) المقابلة الشخصية.\nالتعليم مجاني بالكامل ويمنح الطالب شهادة معترف بها دولياً.",
        "answer_en": "STEM schools are distinguished government schools for students excelling in Science, Technology, Engineering, and Mathematics. Admission requirements:\n1) High score in the Preparatory Certificate.\n2) Passing entrance exams.\n3) Personal interview.\nEducation is completely free and grants an internationally recognized certificate.",
        "category": "مصر",
        "sort_order": 83
    },
    {
        "keywords": "بنك المعرفة المصري, eKB, egyptian knowledge bank, بنك المعرفة, المكتبة الرقمية, منصة التعلم, البحث العلمي, منصة إدمودو, edmodo",
        "answer_ar": "بنك المعرفة المصري (EKB) هو أكبر مكتبة رقمية في العالم أطلقته مصر. يوفر:\n1) آلاف الكتب والمراجع العلمية.\n2) منصات تعليمية تفاعلية.\n3) قنوات تعليمية (مدرستنا 1 و2 و3).\n4) محتوى تعليمي لجميع المراحل.\n5) مصادر بحثية للجامعيين والباحثين.\nجميع الطلاب وأولياء الأمور يمكنهم الدخول مجاناً عن طريق الرقم القومي.",
        "answer_en": "The Egyptian Knowledge Bank (EKB) is the largest digital library in the world, launched by Egypt. It provides:\n1) Thousands of books and scientific references.\n2) Interactive educational platforms.\n3) Educational TV channels (Madrasetna 1, 2, and 3).\n4) Educational content for all stages.\n5) Research resources for university students and researchers.\nAll students and parents can access it for free using the national ID.",
        "category": "مصر",
        "sort_order": 84
    },
    {
        "keywords": "التعليم الأزهري, أزهري, azhar, al azhar, الأزهر الشريف, معاهد أزهرية, ازهر, ازهري, المعاهد الأزهرية",
        "answer_ar": "التعليم الأزهري هو نظام تعليمي تابع للأزهر الشريف في مصر. يشمل:\n1) المعاهد الأزهرية: تدرس المنهج المصري مضافاً إليه المواد الشرعية.\n2) المراحل: ابتدائي أزهري، إعدادي أزهري، ثانوي أزهري.\n3) يتميز بالتركيز على القرآن الكريم والعلوم الشرعية والعربية.\n4) خريجو الثانوية الأزهرية يمكنهم الالتحاق بجامعة الأزهر.\nيمكنك البحث عن المعاهد الأزهرية عبر المنصة.",
        "answer_en": "Al-Azhar education is an educational system under Al-Azhar Al-Sharif in Egypt. It includes:\n1) Azhar Institutes: teach the Egyptian curriculum plus religious subjects.\n2) Stages: Azhari Primary, Azhari Preparatory, Azhari Secondary.\n3) Characterized by focus on the Quran, Islamic sciences, and Arabic.\n4) Azhari secondary graduates can join Al-Azhar University.\nYou can search for Azhar institutes through the platform.",
        "category": "مصر",
        "sort_order": 85
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

        cats = db.session.query(AiKnowledge.category).distinct().all()
        print(f'\nCategories ({len(cats)}):')
        for c in cats:
            cnt = AiKnowledge.query.filter_by(category=c[0]).count()
            print(f'  - {c[0]}: {cnt} entries')


if __name__ == '__main__':
    seed()
