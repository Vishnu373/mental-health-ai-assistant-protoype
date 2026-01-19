import React, { useState, useEffect } from 'react'
import ChatContainer from './components/ChatContainer'
import { generateUserId, generateSessionId } from './api/chat'

function App() {
    const [userId, setUserId] = useState('')
    const [sessionId, setSessionId] = useState('')

    useEffect(() => {
        // Generate or retrieve user ID from localStorage
        let storedUserId = localStorage.getItem('mhelp_user_id')
        if (!storedUserId) {
            storedUserId = generateUserId()
            localStorage.setItem('mhelp_user_id', storedUserId)
        }
        setUserId(storedUserId)

        // Generate new session ID for this visit
        const newSessionId = generateSessionId()
        setSessionId(newSessionId)
    }, [])

    if (!userId || !sessionId) {
        return (
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh',
                fontFamily: 'system-ui, -apple-system, sans-serif',
                color: '#6b7280'
            }}>
                Loading...
            </div>
        )
    }

    return <ChatContainer userId={userId} sessionId={sessionId} />
}

export default App
