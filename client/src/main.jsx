import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import ClerkProviderWithRoutes from './auth/clerk-provider'
import './styles/app.css'

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <BrowserRouter>
            <ClerkProviderWithRoutes>
                <App />
            </ClerkProviderWithRoutes>
        </BrowserRouter>
    </React.StrictMode>
)
