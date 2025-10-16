const API_BASE = 'http://localhost:5000/api';
const sessionId = 'hackathon_user_1';
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const dialogueMessages = document.getElementById('dialogue-messages');
const typingIndicator = document.getElementById('typing-indicator');
const restartBtn = document.getElementById('restart-btn');
const summaryBtn = document.getElementById('summary-btn');

function addMessage(sender, text) {
  const msg = document.createElement('div');
  msg.className = sender === 'user' ? 'user-message' : 'ai-message';
  msg.textContent = text;
  dialogueMessages.appendChild(msg);
  dialogueMessages.scrollTop = dialogueMessages.scrollHeight;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;
  addMessage('user', message);
  userInput.value = '';
  typingIndicator.style.display = 'block';
  try {
    const res = await fetch(`${API_BASE}/message`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({session_id: sessionId, message})
    });
    const data = await res.json();
    typingIndicator.style.display = 'none';
    addMessage('ai', data.ai_response || data.error || 'Error.');
  } catch (e) {
    typingIndicator.style.display = 'none';
    addMessage('ai', 'Server error.');
  }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(); });

restartBtn.addEventListener('click', async () => {
  await fetch(`${API_BASE}/restart`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({session_id: sessionId})
  });
  dialogueMessages.innerHTML = '';
  addMessage('ai', 'Session restarted.');
});

summaryBtn.addEventListener('click', async () => {
  const res = await fetch(`${API_BASE}/summary`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({session_id: sessionId})
  });
  const data = await res.json();
  alert('Progress: ' + JSON.stringify(data.progress));
});
