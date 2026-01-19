const API_URL = import.meta.env.VITE_API_URL

export async function sendMessage(userId, sessionId, message) {
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: message,
                user_id: userId,
                session_id: sessionId,
                model_name: 'claude-haiku-3.5'
            })
        })

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`)
        }

        return await response.json()
    } catch (error) {
        console.error('Failed to send message:', error)
        throw error
    }
}

export function generateUserId() {
    // Generate a simple UUID v4
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = Math.random() * 16 | 0
        const v = c === 'x' ? r : (r & 0x3 | 0x8)
        return v.toString(16)
    })
}

export function generateSessionId() {
    const timestamp = Date.now()
    const random = Math.random().toString(36).substring(2, 15)
    return `session-${timestamp}-${random}`
}
