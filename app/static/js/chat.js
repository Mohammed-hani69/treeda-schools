/* ═══════════════════════════════════════════════════
   AI Chat Assistant — Treeda Expo
   ═══════════════════════════════════════════════════ */

const aiKnowledge = [
  { keywords: ['مرحبا', 'السلام', 'hi', 'hello', 'اهلا'], answer: 'وعليكم السلام! 👋 أنا مساعد تريدا أكسبو الذكي. كيف يمكنني مساعدتك؟' },
  { keywords: ['شكرا', 'thanks', 'thank'], answer: 'العفو! 😊 نحن في خدمتك دائماً.' },
  { keywords: ['المنصة', 'عن', 'what is', 'منصة'], answer: '🏫 تريدا أكسبو (Treeda Expo) هو المعرض الافتراضي الأول للمدارس في المملكة. نمنح المدارس فرصة مميزة لعرض تفاصيلها والاتصال المباشر بأولياء الأمور، ونساعد أولياء الأمور على المقارنة واختيار المدرسة الأنسب.' },
  { keywords: ['تسجيل', 'اشتراك', 'حساب', 'register', 'sign'], answer: '📝 للتسجيل كمدرسة: اضغط على "سجل مدرستك الآن" واختر الباقة المناسبة.\n📝 للتسجيل كولي أمر: اضغط على "إنشاء حساب" واملأ بياناتك.\nالتسجيل مجاني لأولياء الأمور!' },
  { keywords: ['باقه', 'باقة', 'سعر', 'price', 'plan', 'pricing', 'سع', 'خطط'], answer: '💰 باقات الاشتراك:\n• البرونزية: $99/شهر - للمدارس الناشئة\n• الذهبية: $249/شهر - الأكثر طلباً 🏆\n• الماسية: $499/شهر - حل متكامل\nجميع الباقات تشمل فترة تجربة مجانية!' },
  { keywords: ['مميزات', 'features', 'خصائص', 'تتميز'], answer: '✨ مميزات المنصة:\n• ملف تعريفي احترافي لكل مدرسة\n• صور وفيديوهات عالية الجودة\n• جولات افتراضية ثلاثية الأبعاد\n• تواصل مباشر مع الإدارة\n• نظام حجز مواعيد\n• فلاتر بحث ذكية' },
  { keywords: ['اتصال', 'رقم', 'تواصل', 'واتس', 'phone', 'call', 'contact'], answer: '📞 معلومات التواصل:\n• الهاتف: 01097000010\n• البريد: support@treedaexpo.com\n• العنوان: القاهره\n• متاحون يومياً من ٩ صباحاً إلى ٩ مساءً' },
  { keywords: ['المدارس', 'schools', 'مدرسة', 'مدارس'], answer: '🏫 لدينا العديد من المدارس المسجلة في المنصة، تشمل:\n• المدارس الدولية (IGCSE, IB)\n• المدارس الخاصة\n• المدارس التجريبية\n• رياض الأطفال والحضانات\n• مراكز التدريب\nيمكنك تصفحها جميعاً في قسم "المدارس المميزة"' },
  { keywords: ['كيف', 'how', 'طريقة', 'طريقه'], answer: '✅ استخدام المنصة سهل جداً:\n1️⃣ سجل حساباً جديداً (أولياء أمور مجاناً)\n2️⃣ ابحث عن المدارس باستخدام الفلاتر\n3️⃣ تصفح الملفات التعريفية والصور\n4️⃣ تواصل مباشر مع الإدارة أو احجز زيارة' },
  { keywords: ['دفع', 'payment', 'pay', 'فيزا', 'credit'], answer: '💳 طرق الدفع المتاحة:\n• البطاقات الائتمانية (Visa, Mastercard)\n• التحويل البنكي المباشر\n• محافظ الدفع الإلكتروني\nجميع المعاملات مشفرة وآمنة 100%.' },
  { keywords: ['ادمن', 'admin', 'مدير'], answer: '🔐 لوحة التحكم الخاصة بالإدارة تتيح:\n• إدارة المدارس والطلبات\n• الموافقة على المحتوى\n• إدارة الباقات والاشتراكات\n• إعدادات المنصة\n• تقارير وإحصائيات' }
];

function findAnswer(msg) {
  const m = msg.toLowerCase();
  for (const item of aiKnowledge) {
    for (const kw of item.keywords) {
      if (m.includes(kw)) return item.answer;
    }
  }
  return null;
}

function openChat() {
  const panel = document.getElementById('aiChatPanel');
  const btn = document.getElementById('aiChatBtn');
  if (panel) { panel.style.display = 'flex'; panel.style.opacity = '1'; }
  if (btn) { btn.style.display = 'none'; }
  setTimeout(() => {
    const msgArea = document.getElementById('aiChatMessages');
    if (msgArea && !msgArea.querySelector('.chat-msg-bot')) {
      addMessage('bot', '👋 مرحباً! أنا مساعد تريدا أكسبو الذكي. أسألني عن المنصة، الباقات، التسجيل، أو أي شيء تريد معرفته!');
    }
  }, 300);
}

function closeChat() {
  const panel = document.getElementById('aiChatPanel');
  const btn = document.getElementById('aiChatBtn');
  if (panel) { panel.style.display = 'none'; }
  if (btn) { btn.style.display = 'flex'; }
}

function addMessage(type, text) {
  const area = document.getElementById('aiChatMessages');
  if (!area) return;
  const div = document.createElement('div');
  div.className = 'chat-msg chat-msg-' + type;
  div.textContent = text;
  area.appendChild(div);
  area.scrollTop = area.scrollHeight;
}

function sendChatMessage() {
  const input = document.getElementById('aiChatInput');
  const msg = input.value.trim();
  if (!msg) return;
  addMessage('user', msg);
  input.value = '';
  setTimeout(() => {
    const answer = findAnswer(msg);
    if (answer) {
      addMessage('bot', answer);
    } else {
      addMessage('bot', '🤔 لم أجد إجابة محددة لسؤالك. يمكنك التواصل معنا عبر الهاتف 01097000010 أو مراسلتنا عبر نموذج الاتصال في الأسفل.');
    }
  }, 400);
}

document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('aiChatInput');
  if (input) {
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') sendChatMessage();
    });
  }
});
