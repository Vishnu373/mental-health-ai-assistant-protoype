import React from 'react'
import { SignIn } from '@clerk/clerk-react'

const SignInPage = () => {
    return (
        <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '100vh',
            backgroundColor: '#343541', // ChatGPT dark background
        }}>
            <SignIn
                path="/sign-in"
                routing="path"
                signUpUrl="/sign-up"
                appearance={{
                    variables: {
                        colorPrimary: '#10a37f', // ChatGPT green
                        colorText: '#ffffff',
                        colorBackground: '#202123', // Darker card background
                        colorInputBackground: '#343541',
                        colorInputText: '#ffffff',
                    },
                    elements: {
                        rootBox: {
                            boxShadow: 'none',
                        },
                        card: {
                            border: '1px solid #4d4d4f',
                            boxShadow: '0 0 10px rgba(0,0,0,0.5)',
                        }
                    }
                }}
            />
        </div>
    )
}

export default SignInPage
