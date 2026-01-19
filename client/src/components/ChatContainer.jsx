import React, { useState } from 'react'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import { sendMessage } from '../api/chat'

function ChatContainer({ userId, sessionId }) {
    const [messages, setMessages] = useState([
        {
            id: 1,
            sender: 'assistant',
            content: 'Hello! I\'m MhelpAI, your mental health support assistant. Feel free to share what\'s on your mind, and I\'ll do my best to help.\n\n**Note:** I\'m an AI assistant and not a replacement for professional mental health care. If you\'re experiencing a crisis, please contact emergency services or a mental health hotline immediately.',
            timestamp: new Date()
        }
    ])
    const [isLoading, setIsLoading] = useState(false)

    const handleSendMessage = async (messageText) => {
        // Add user message
        const userMessage = {
            id: Date.now(),
            sender: 'user',
            content: messageText,
            timestamp: new Date()
        }
        setMessages(prev => [...prev, userMessage])
        setIsLoading(true)

        try {
            const response = await sendMessage(userId, sessionId, messageText)

            // Add AI response
            const aiMessage = {
                id: Date.now() + 1,
                sender: 'assistant',
                content: response.response,
                timestamp: new Date()
            }
            setMessages(prev => [...prev, aiMessage])
        } catch (error) {
            // Add error message
            const errorMessage = {
                id: Date.now() + 1,
                sender: 'error',
                content: 'Sorry, I encountered an error. Please try again.',
                timestamp: new Date()
            }
            setMessages(prev => [...prev, errorMessage])
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h1>MhelpAI</h1>
                <p>Mental Health Assistant</p>
            </div>
            <MessageList messages={messages} isLoading={isLoading} />
            <MessageInput onSendMessage={handleSendMessage} disabled={isLoading} />
        </div>
    )
}

export default ChatContainer
