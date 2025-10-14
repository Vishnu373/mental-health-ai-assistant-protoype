import { Clerk } from '@clerk/clerk-js'
import { initializeChat, showChatInterface } from './chat.js'
import { showAuthInterface } from './auth.js'
import { loadTemplate, renderTemplate } from './templateLoader.js'

// Application state
let clerk = null
let currentUser = null
let sessionId = null

// Get Clerk publishable key
const clerkPubKey = import.meta.env.VITE_CLERK_KEY

async function initializeApp() {
    try {
        console.log('Initializing Mental Health AI Assistant...')
        
        if (!clerkPubKey) {
            throw new Error('Missing Clerk Publishable Key')
        }

        // Initialize Clerk
        clerk = new Clerk(clerkPubKey)
        await clerk.load()

        // Set up auth state listener
        clerk.addListener(({ user }) => {
            const wasAuthenticated = currentUser !== null
            const isAuthenticated = user !== null
            
            currentUser = user
            
            // Only re-render if authentication state actually changed
            if (wasAuthenticated !== isAuthenticated) {
                renderApp()
            }
        })

        // Initial render
        currentUser = clerk.user
        renderApp()

        console.log('App initialized successfully!')
    } catch (error) {
        console.error('Error initializing app:', error)
        showError('Failed to initialize the application', error.message)
    }
}

async function renderApp() {
    if (currentUser) {
        // User is authenticated - show chat interface
        console.log('User authenticated:', currentUser.id)
        sessionId = generateSessionId()
        await showChatInterface(currentUser)
        initializeChat()
    } else {
        // User not authenticated - show auth interface
        console.log('User not authenticated, showing auth interface')
        await showAuthInterface(clerk)
    }
}

function generateSessionId() {
    const userId = currentUser?.id || 'anonymous'
    const timestamp = Date.now()
    const random = Math.random().toString(36).substring(2)
    return `${userId}-${timestamp}-${random}`
}

async function showError(title, message) {
    try {
        const template = await loadTemplate('error')
        const renderedHTML = renderTemplate(template, { title, message })
        document.getElementById('app').innerHTML = renderedHTML
    } catch (error) {
        // Fallback if template loading fails
        console.error('Error loading error template:', error)
        document.getElementById('app').innerHTML = `
            <div style="color: red; text-align: center; padding: 2rem;">
                <h2>${title}</h2>
                <p>${message}</p>
                <button onclick="location.reload()">Reload Page</button>
            </div>
        `
    }
}

window.handleSendMessage = async function(message) {
    if (!currentUser || !sessionId) {
        console.error('User not authenticated or missing session')
        return
    }

    try {
        // API call logic will be imported from chat.js
        const response = await fetch('https://mhelp-ai-backend.onrender.com/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: message,
                user_id: currentUser.id,
                session_id: sessionId,
                model_name: 'gpt-4'
            })
        })

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`)
        }

        const result = await response.json()
        return result
    } catch (error) {
        console.error('Error sending message:', error)
        throw error
    }
}

window.handleSignOut = async function() {
    try {
        if (clerk) {
            await clerk.signOut()
        }
    } catch (error) {
        console.error('Error signing out:', error)
    }
}

export { currentUser, sessionId }

document.addEventListener('DOMContentLoaded', initializeApp)