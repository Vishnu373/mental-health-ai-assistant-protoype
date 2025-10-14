import { loadTemplate, renderTemplate } from './templateLoader.js';

// Show chat interface
export async function showChatInterface(user) {
    try {
        const app = document.getElementById('app')
        const userName = getUserDisplayName(user)
        
        // Load and render template with user data
        const template = await loadTemplate('chat')
        const renderedHTML = renderTemplate(template, { userName })
        
        app.innerHTML = renderedHTML
    } catch (error) {
        console.error('Error loading chat template:', error)
        // Fallback to basic error message
        document.getElementById('app').innerHTML = '<div>Error loading chat interface</div>'
    }
}

// Initialize chat functionality
export function initializeChat() {
    const chatInput = document.getElementById('chatInput')
    const sendButton = document.getElementById('sendButton')
    
    if (!chatInput || !sendButton) {
        console.error('Chat elements not found')
        return
    }
    
    // Auto-resize textarea
    chatInput.addEventListener('input', function() {
        this.style.height = 'auto'
        this.style.height = Math.min(this.scrollHeight, 120) + 'px'
    })
    
    // Handle Enter key (send message, Shift+Enter for new line)
    chatInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    })
    
    // Enable/disable send button based on input
    chatInput.addEventListener('input', function() {
        sendButton.disabled = !this.value.trim()
    })
    
    console.log('Chat initialized successfully')
}

// Send a message to the AI assistant
window.sendMessage = async function() {
    const chatInput = document.getElementById('chatInput')
    const sendButton = document.getElementById('sendButton')
    const chatMessages = document.getElementById('chatMessages')
    
    const message = chatInput.value.trim()
    if (!message) return
    
    // Disable input while processing
    chatInput.disabled = true
    sendButton.disabled = true
    sendButton.textContent = 'Sending...'
    
    try {
        // Add user message to chat
        addMessageToChat('user', message)
        
        // Clear input
        chatInput.value = ''
        chatInput.style.height = 'auto'
        
        // Add typing indicator
        addTypingIndicator()
        
        // Send message to API using the global handler
        const response = await window.handleSendMessage(message)
        
        // Remove typing indicator
        removeTypingIndicator()
        
        // Add AI response to chat
        if (response.response) {
            addMessageToChat('assistant', response.response)
        } else {
            throw new Error('No response received from AI')
        }
        
    } catch (error) {
        console.error('Error sending message:', error)
        removeTypingIndicator()
        addMessageToChat('error', 'Sorry, I encountered an error. Please try again.')
    } finally {
        // Re-enable input
        chatInput.disabled = false
        sendButton.disabled = false
        sendButton.textContent = 'Send'
        chatInput.focus()
    }
}

// Add a message to the chat display
function addMessageToChat(sender, content) {
    const chatMessages = document.getElementById('chatMessages')
    const messageDiv = document.createElement('div')
    messageDiv.className = `message ${sender}-message`
    
    const timestamp = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <span class="message-sender">${sender === 'user' ? 'You' : 'MhelpAI'}</span>
            <span class="message-time">${timestamp}</span>
        </div>
        <div class="message-content">${content}</div>
    `
    
    chatMessages.appendChild(messageDiv)
    chatMessages.scrollTop = chatMessages.scrollHeight
}

// Add typing indicator
function addTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages')
    const typingDiv = document.createElement('div')
    typingDiv.className = 'message assistant-message typing-indicator'
    typingDiv.id = 'typingIndicator'
    
    typingDiv.innerHTML = `
        <div class="message-header">
            <span class="message-sender">MhelpAI</span>
        </div>
        <div class="message-content">
            <div class="typing-animation">
                <span></span><span></span><span></span>
            </div>
        </div>
    `
    
    chatMessages.appendChild(typingDiv)
    chatMessages.scrollTop = chatMessages.scrollHeight
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator')
    if (typingIndicator) {
        typingIndicator.remove()
    }
}

// Get user display name
function getUserDisplayName(user) {
    if (!user) return 'User'
    
    const firstName = user.firstName || ''
    const lastName = user.lastName || ''
    const fullName = `${firstName} ${lastName}`.trim()
    
    if (fullName) return fullName
    if (user.emailAddresses && user.emailAddresses.length > 0) {
        return user.emailAddresses[0].emailAddress
    }
    
    return 'User'
}