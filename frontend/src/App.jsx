import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles } from 'lucide-react';

function App() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isTyping]);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = input.trim();
        setMessages(prev => [...prev, { text: userMessage, isUser: true }]);
        setInput('');
        setIsTyping(true);

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage }),
            });

            const data = await response.json();
            setMessages(prev => [...prev, { text: data.response, isUser: false }]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, { text: "Failed to connect to the server. Please ensure the backend is running.", isUser: false }]);
        } finally {
            setIsTyping(false);
        }
    };

    const sendSuggestion = (text) => {
        setInput(text);
        // Auto-submit if needed, or just set input
    };

    return (
        <div className="app-container">
            <div className="chat-box">
                <header>
                    <div className="logo">
                        <div className="logo-icon"></div>
                        <h1>Enterprise Support</h1>
                    </div>
                    <div className="status-badge">
                        <span className="status-dot"></span> Online
                    </div>
                </header>

                <main className="chat-messages">
                    {messages.length === 0 ? (
                        <div className="welcome-screen">
                            <Sparkles size={48} className="icon-pulse" style={{ color: 'var(--primary)', marginBottom: '1rem' }} />
                            <h2>How can I help you today?</h2>
                            <p>I'm your AI support assistant, trained on our latest product documentation.</p>
                            <div className="suggestions">
                                <button className="suggestion-btn" onClick={() => sendSuggestion('Specs for TechGizmo Pro X1')}>TechGizmo Specs</button>
                                <button className="suggestion-btn" onClick={() => sendSuggestion('Check warranty SN-X19876')}>Warranty Check</button>
                                <button className="suggestion-btn" onClick={() => sendSuggestion('How to setup SmartHome Hub')}>Setup Guide</button>
                            </div>
                        </div>
                    ) : (
                        <>
                            {messages.map((msg, index) => (
                                <div key={index} className={`message ${msg.isUser ? 'user-message' : 'bot-message'}`}>
                                    <div className="message-content">
                                        {msg.text}
                                    </div>
                                </div>
                            ))}
                            {isTyping && (
                                <div className="typing-indicator">
                                    <span></span><span></span><span></span>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </>
                    )}
                </main>

                <footer>
                    <form className="input-area" onSubmit={handleSendMessage}>
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type your message..."
                            autoComplete="off"
                        />
                        <button type="submit" className="send-btn" disabled={isTyping || !input.trim()}>
                            <Send size={20} />
                        </button>
                    </form>
                </footer>
            </div>
        </div>
    );
}

export default App;
