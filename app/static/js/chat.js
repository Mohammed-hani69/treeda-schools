/* ═══════════════════════════════════════════════════
   AI Chat Assistant — Treeda Expo
   Dynamic: fetches answers from server API
   ═══════════════════════════════════════════════════ */

function getLang() {
  const html = document.documentElement;
  return html.getAttribute('lang') || 'ar';
}

async function fetchAnswer(msg) {
  try {
    const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg, lang: getLang() })
    });
    const data = await resp.json();
    return data.answer || null;
  } catch {
    return null;
  }
}

function openChat() {
  const panel = document.getElementById('aiChatPanel');
  const btn = document.getElementById('aiChatBtn');
  if (panel) { panel.style.display = 'flex'; panel.style.opacity = '1'; }
  if (btn) { btn.style.display = 'none'; }
  setTimeout(() => {
    const msgArea = document.getElementById('aiChatMessages');
    if (msgArea && !msgArea.querySelector('.chat-msg-bot')) {
      const greeting = getLang() === 'en'
        ? '👋 Hello! I am the Treeda Expo AI assistant. Ask me about the platform, plans, registration, or anything you\'d like to know!'
        : '👋 مرحباً! أنا مساعد تريدا أكسبو الذكي. أسألني عن المنصة، الباقات، التسجيل، أو أي شيء تريد معرفته!';
      addMessage('bot', greeting);
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

async function sendChatMessage() {
  const input = document.getElementById('aiChatInput');
  const msg = input.value.trim();
  if (!msg) return;
  addMessage('user', msg);
  input.value = '';
  const typingMsg = document.createElement('div');
  typingMsg.className = 'chat-msg chat-msg-bot';
  typingMsg.textContent = '...';
  typingMsg.id = 'typingIndicator';
  document.getElementById('aiChatMessages').appendChild(typingMsg);
  const answer = await fetchAnswer(msg);
  const indicator = document.getElementById('typingIndicator');
  if (indicator) indicator.remove();
  addMessage('bot', answer || (getLang() === 'en'
    ? '🤔 I couldn\'t find a specific answer. Please contact us at +201097000010 or use the contact form below.'
    : '🤔 لم أجد إجابة محددة لسؤالك. يمكنك التواصل معنا عبر الهاتف 01097000010 أو مراسلتنا عبر نموذج الاتصال في الأسفل.'));
}

document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('aiChatInput');
  if (input) {
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') sendChatMessage();
    });
  }
});
