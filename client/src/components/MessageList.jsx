import React, { useEffect, useRef } from 'react'
import { marked } from 'marked'

function MessageList({ messages, isLoading }) {
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages, isLoading])

    const formatTime = (date) => {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }

    return (
        <div className="message-list">
            {messages.map((message) => (
                <div key={message.id} className={`message ${message.sender}-message`}>
                    <div className="message-header">
                        <span className="message-sender">
                            {message.sender === 'user' ? 'You' : message.sender === 'error' ? 'System' : 'MhelpAI'}
                        </span>
                        <span className="message-time">{formatTime(message.timestamp)}</span>
                    </div>
                    <div
                        className="message-content"
                        dangerouslySetInnerHTML={{
                            __html: message.sender === 'assistant'
                                ? marked.parse(message.content)
                                : message.content
                        }}
                    />
                </div>
            ))}

            {isLoading && (
                <div className="message assistant-message typing-indicator">
                    <div className="message-header">
                        <span className="message-sender">MhelpAI</span>
                    </div>
                    <div className="message-content">
                        <div className="typing-animation">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
            )}

            <div ref={messagesEndRef} />
        </div>
    )
}

export default MessageList
