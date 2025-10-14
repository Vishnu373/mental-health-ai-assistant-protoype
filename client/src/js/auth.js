// Show authentication interface
export function showAuthInterface(clerk) {
    const app = document.getElementById('app')
    
    app.innerHTML = `
        <div class="auth-container">
            <div class="auth-content">
                <h1 class="auth-title">Mental Health AI Assistant</h1>
                <h2 class="auth-subtitle">MhelpAI</h2>
                <p class="auth-description">Your AI companion for mental health support and guidance.</p>
                <p class="auth-disclaimer">This is a prototype only.</p>
                <div id="clerk-auth" class="clerk-auth-container"></div>
            </div>
        </div>
    `

    // Mount Clerk authentication component
    const authContainer = document.getElementById('clerk-auth')
    if (clerk && authContainer) {
        clerk.mountSignIn(authContainer)
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