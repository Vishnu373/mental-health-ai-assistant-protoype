/** Message list component - displays chat messages. */
import React, { useEffect, useRef } from 'react'
import { marked } from 'marked'
import { useUser } from '@clerk/clerk-react'

function MessageList({ messages, isLoading }) {
    const messagesEndRef = useRef(null)
    const { user } = useUser()

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages, isLoading])

    return (
        <div className="message-list">
            {messages.map((message) => (
                <div key={message.id} className={`message-row ${message.sender}`}>
                    <div className="message-content-container">
                        <div className={`avatar ${message.sender}`}>
                            {message.sender === 'user' ? (
                                <img
                                    src={user?.imageUrl || 'https://via.placeholder.com/30'}
                                    alt="User"
                                    style={{ width: '100%', height: '100%', borderRadius: '4px' }}
                                />
                            ) : (
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    <path d="M2 17L12 22L22 17" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    <path d="M2 12L12 17L22 12" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            )}
                        </div>
                        <div
                            className="message-text"
                            dangerouslySetInnerHTML={{
                                __html: message.sender === 'assistant'
                                    ? marked.parse(message.content)
                                    : message.content
                            }}
                        />
                    </div>
                </div>
            ))}

            {isLoading && (
                <div className="message-row assistant">
                    <div className="message-content-container">
                        <div className="avatar assistant">
                            <div className="typing-dots">
                                <span></span><span></span><span></span>
                            </div>
                        </div>
                        <div className="message-text"></div>
                    </div>
                </div>
            )}

            <div ref={messagesEndRef} />
        </div>
    )
}

export default MessageList
