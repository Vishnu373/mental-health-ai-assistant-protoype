import { loadTemplate, renderTemplate } from './templateLoader.js';

// Show authentication interface
export async function showAuthInterface(clerk) {
    try {
        const app = document.getElementById('app')
        
        // Load and render template
        const template = await loadTemplate('auth')
        const renderedHTML = renderTemplate(template)
        
        app.innerHTML = renderedHTML

        // Mount Clerk authentication component
        const authContainer = document.getElementById('clerk-auth')
        if (clerk && authContainer) {
            clerk.mountSignIn(authContainer)
        }
    } catch (error) {
        console.error('Error loading auth template:', error)
        // Fallback to basic error message
        document.getElementById('app').innerHTML = '<div>Error loading authentication page</div>'
    }
}

// Show welcome message after successful authentication
export function showWelcomeMessage(user) {
    const app = document.getElementById('app')
    
    app.innerHTML = `
        <div class="welcome-container">
            <div class="welcome-content">
                <h1 class="welcome-title">Welcome to MhelpAI!</h1>
                <h2 class="welcome-subtitle">Hello, ${user.firstName || 'User'}!</h2>
                <p class="welcome-message">You are successfully signed in.</p>
                <p class="welcome-redirect">Redirecting to chat interface...</p>
                <div class="loading-spinner"></div>
            </div>
        </div>
    `
}