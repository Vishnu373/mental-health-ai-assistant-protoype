import { Clerk } from '@clerk/clerk-js'

// Get Clerk publishable key with fallback
const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY || 'pk_test_YWRhcHRpbmctcHJhd24tMS5jbGVyay5hY2NvdW50cy5kZXYk'

if (!clerkPubKey) {
  document.getElementById('app').innerHTML = `
    <div style="color: red; text-align: center; padding: 2rem;">
      <h2>Configuration Error</h2>
      <p>Clerk Publishable Key is missing. Please check your environment configuration.</p>
    </div>
  `
  throw new Error('Missing Clerk Publishable Key')
}

try {
  const clerk = new Clerk(clerkPubKey)
  await clerk.load()

  if (clerk.user) {
    // User is signed in
    document.getElementById('app').innerHTML = `
      <div style="text-align: center; padding: 2rem;">
        <h2>Welcome!</h2>
        <p>You are successfully signed in.</p>
        <div id="user-button"></div>
      </div>
    `

    const userButtonDiv = document.getElementById('user-button')
    clerk.mountUserButton(userButtonDiv)
  } else {
    // User is not signed in
    document.getElementById('app').innerHTML = `
      <div style="text-align: center; padding: 2rem;">
        <h2>Mental Health AI Assistant</h2>
        <p>Please sign in to continue</p>
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
        <div style="text-align: center; padding: 2rem;">
          <h2>Welcome!</h2>
          <p>You are successfully signed in.</p>
          <div id="user-button"></div>
        </div>
      `
      const userButtonDiv = document.getElementById('user-button')
      clerk.mountUserButton(userButtonDiv)
    } else {
      // User signed out
      document.getElementById('app').innerHTML = `
        <div style="text-align: center; padding: 2rem;">
          <h2>Mental Health AI Assistant</h2>
          <p>Please sign in to continue</p>
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
      <p>Failed to initialize authentication system. Please refresh the page.</p>
      <p><small>${error.message}</small></p>
    </div>
  `
}
