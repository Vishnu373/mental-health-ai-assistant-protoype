import { Clerk } from '@clerk/clerk-js'

// Get Clerk publishable key with fallback
const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY || 'pk_test_YWRhcHRpbmctcHJhd24tMS5jbGVyay5hY2NvdW50cy5kZXYk'

if (!clerkPubKey) {
  document.getElementById('app').innerHTML = `
    <div style="color: red; text-align: center; padding: 2rem;">
      <h2>Configuration Error</h2>
      <p>Clerk Publishable Key is missing.</p>
    </div>
  `
  throw new Error('Missing Clerk Publishable Key')
}

try {
  const clerk = new Clerk(clerkPubKey)
  await clerk.load()

  if (clerk.user) {
    // User is signed in - show welcome + user button
    document.getElementById('app').innerHTML = `
      <div style="text-align: center; padding: 2rem; color: white;">
        <h1>Mental Health AI Assistant (MhelpAI)</h1>
        <h2>Welcome, ${clerk.user.firstName || 'User'}!</h2>
        <p>You are successfully signed in.</p>
        <div id="user-button" style="margin-top: 2rem;"></div>
      </div>
    `

    const userButtonDiv = document.getElementById('user-button')
    clerk.mountUserButton(userButtonDiv)
  } else {
    // User is not signed in - show sign in page
    document.getElementById('app').innerHTML = `
      <div style="text-align: center; padding: 2rem; color: white;">
        <h1>Mental Health AI Assistant (MhelpAI)</h1>
        <p style="margin: 1rem 0;">Your AI companion for mental health support and guidance.</p>
        <p style="font-style: italic; color: #888; margin-bottom: 2rem;">This is a prototype only.</p>
        <div id="sign-in"></div>
      </div>
    `

    const signInDiv = document.getElementById('sign-in')
    clerk.mountSignIn(signInDiv)
  }

  // Listen for auth state changes
  clerk.addListener(({ user }) => {
    if (user) {
      // User signed in
      document.getElementById('app').innerHTML = `
        <div style="text-align: center; padding: 2rem; color: white;">
          <h1>Mental Health AI Assistant (MhelpAI)</h1>
          <h2>Welcome, ${user.firstName || 'User'}!</h2>
          <p>You are successfully signed in.</p>
          <div id="user-button" style="margin-top: 2rem;"></div>
        </div>
      `
      const userButtonDiv = document.getElementById('user-button')
      clerk.mountUserButton(userButtonDiv)
    } else {
      // User signed out - show sign in page
      document.getElementById('app').innerHTML = `
        <div style="text-align: center; padding: 2rem; color: white;">
          <h1>Mental Health AI Assistant (MhelpAI)</h1>
          <p style="margin: 1rem 0;">Your AI companion for mental health support and guidance.</p>
          <p style="font-style: italic; color: #888; margin-bottom: 2rem;">This is a prototype only.</p>
          <div id="sign-in"></div>
        </div>
      `
      const signInDiv = document.getElementById('sign-in')
      clerk.mountSignIn(signInDiv)
    }
  })

} catch (error) {
  console.error('Clerk initialization error:', error)
  document.getElementById('app').innerHTML = `
    <div style="color: red; text-align: center; padding: 2rem;">
      <h2>Authentication Error</h2>
      <p>Failed to load authentication. Please refresh the page.</p>
      <p><small>${error.message}</small></p>
    </div>
  `
}
