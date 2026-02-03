/** Chat container - main chat interface component. */
import React, { useState } from 'react'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import { sendMessage } from '../api/chat'
import { UserButton, useUser } from '@clerk/clerk-react'

function ChatContainer({ userId, sessionId }) {
    const { user } = useUser()
    const [messages, setMessages] = useState([
        {
            id: 1,
            sender: 'assistant',
            content: 'Hello! I\'m MhelpAI, your mental health support assistant. Feel free to share what\'s on your mind.',
            timestamp: new Date()
        }
    ])
    const [isLoading, setIsLoading] = useState(false)
    const [contextProgress, setContextProgress] = useState(10)

    const handleSendMessage = async (messageText) => {
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
            const aiMessage = {
                id: Date.now() + 1,
                sender: 'assistant',
                content: response.response,
                timestamp: new Date()
            }
            setMessages(prev => [...prev, aiMessage])
            setContextProgress(prev => Math.min(prev + 5, 100))
        } catch (error) {
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
            <div className="chat-status-bar">
                <div
                    className="context-indicator"
                    style={{ '--progress': `${contextProgress}%` }}
                    title={`Context Collected: ${contextProgress}%`}
                >
                    <span className="context-tooltip">{contextProgress}% Context</span>
                </div>
                <UserButton afterSignOutUrl="/sign-in" />
            </div>

            <MessageList messages={messages} isLoading={isLoading} />
            <MessageInput onSendMessage={handleSendMessage} disabled={isLoading} />
        </div>
    )
}

export default ChatContainer
