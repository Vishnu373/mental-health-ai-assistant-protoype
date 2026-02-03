import React, { useState, useEffect } from 'react'
import ChatContainer from '../components/ChatContainer'
import { generateUserId, generateSessionId } from '../api/chat'
import { useUser } from '@clerk/clerk-react'

function ChatPage() {
    const { user } = useUser()
    const [userId, setUserId] = useState('')
    const [sessionId, setSessionId] = useState('')

    useEffect(() => {
        if (user) {
            setUserId(user.id)
        }

        // Generate new session ID for this visit
        const newSessionId = generateSessionId()
        setSessionId(newSessionId)
    }, [user])

    if (!userId || !sessionId) {
        return (
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh',
                fontFamily: 'system-ui, -apple-system, sans-serif',
                color: '#6b7280',
                backgroundColor: '#343541' // Match theme
            }}>
                Loading...
            </div>
        )
    }

    return <ChatContainer userId={userId} sessionId={sessionId} />
}

export default ChatPage
