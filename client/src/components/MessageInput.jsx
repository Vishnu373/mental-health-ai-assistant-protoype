import React, { useState, useRef } from 'react'

function MessageInput({ onSendMessage, disabled }) {
    const [message, setMessage] = useState('')
    const textareaRef = useRef(null)

    const handleSubmit = (e) => {
        e.preventDefault()
        if (message.trim() && !disabled) {
            onSendMessage(message.trim())
            setMessage('')
            // Reset textarea height
            if (textareaRef.current) {
                textareaRef.current.style.height = 'auto'
            }
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSubmit(e)
        }
    }

    const handleChange = (e) => {
        setMessage(e.target.value)
        // Auto-resize textarea
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto'
            textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px'
        }
    }

    return (
        <form className="message-input-container" onSubmit={handleSubmit}>
            <textarea
                ref={textareaRef}
                className="message-input"
                placeholder="Type your message here..."
                value={message}
                onChange={handleChange}
                onKeyDown={handleKeyDown}
                disabled={disabled}
                rows={1}
            />
            <button
                type="submit"
                className="send-button"
                disabled={disabled || !message.trim()}
            >
                {disabled ? 'Sending...' : 'Send'}
            </button>
        </form>
    )
}

export default MessageInput
