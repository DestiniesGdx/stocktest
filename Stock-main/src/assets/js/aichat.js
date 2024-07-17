document.getElementById('send-button').addEventListener('click', sendMessage);
appendMessage('你好！有什么关于股市的问题我可以帮助你吗？');
function sendMessage() {
    var userMessage = document.getElementById('user-input').value;
    document.getElementById('user-input').value = '';

    appendMessage(userMessage, 'user');

    fetch('http://127.0.0.1:5000/aichat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
    })
    .then(response => response.json())
    .then(data => {
        appendMessage(data.response, 'ai');
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function appendMessage(message, sender) {
    var chatLog = document.getElementById('chat-log');
    var messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.textContent = message;

    if (sender === 'user') {
        messageDiv.classList.add('user-message');
    } else {
        messageDiv.classList.add('ai-message');
    }

    chatLog.appendChild(messageDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
}
