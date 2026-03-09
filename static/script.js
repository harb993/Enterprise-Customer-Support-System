const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const messagesContainer = document.getElementById('messages');
const chatWindow = document.getElementById('chat-window');
const typingIndicator = document.getElementById('typing-indicator');
const welcomeSection = document.querySelector('.welcome-message');

function addMessage(text, isUser = false) {
    if (welcomeSection) {
        welcomeSection.classList.add('hidden');
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = text;
    messagesContainer.appendChild(messageDiv);

    // Smooth scroll to bottom
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendRequest(message) {
    typingIndicator.classList.remove('hidden');
    chatWindow.scrollTop = chatWindow.scrollHeight;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        typingIndicator.classList.add('hidden');
        addMessage(data.response);
    } catch (error) {
        typingIndicator.classList.add('hidden');
        addMessage("Sorry, I'm having trouble connecting to the server.", false);
        console.error('Error:', error);
    }
}

chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (message) {
        addMessage(message, true);
        userInput.value = '';
        sendRequest(message);
    }
});

function sendSuggestion(text) {
    addMessage(text, true);
    sendRequest(text);
}
