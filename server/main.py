import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models.chats_pym import ChatInput
from modes.conversation import Conversation
from modes.info_collection import InfoCollectionMode
from datetime import datetime

app = FastAPI(title="Mental Health AI Assistant API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Mental Health AI Assistant API is running"}

active_sessions = {}

# Same for signup as well
@app.post("/login")
def login_endpoint(chat_input: ChatInput):
    user_id = chat_input.user_id
    
    # Create new session
    conversation = Conversation(user_id)
    session_id = conversation.start_session()
    
    # Store in active sessions
    active_sessions[user_id] = session_id
    
    # Hardcoded welcome message
    welcome_message = "Hi. I'm here to help support your mental well-being. To get started, I'd love to learn a bit about you. Could you tell me your name and a little about what brings you here today?"
    
    return {
        "session_id": session_id,
        "user_id": user_id,
        "message": welcome_message
    }

@app.post("/chat")
def chat_endpoint(chat_input: ChatInput):
    user_id = chat_input.user_id
    query = chat_input.query
    
    # Check if user has active session
    session_id = active_sessions.get(user_id)
    if not session_id:
        raise HTTPException(status_code=400, detail="No active session. Please login first.")
    
    # Create InfoCollectionMode instance
    info_mode = InfoCollectionMode(user_id, session_id)
    
    # Call run_pipeline
    response = info_mode.run_pipeline(query)
    
    return {"response": response}

@app.post("/logout")
def logout_endpoint(chat_input: ChatInput):
    user_id = chat_input.user_id
    
    # Get session_id from active_sessions
    session_id = active_sessions.get(user_id)
    if not session_id:
        raise HTTPException(status_code=400, detail="No active session found.")
    
    # Create Conversation instance and set session_id
    conv = Conversation(user_id)
    conv.session_id = session_id
    
    # Generate and save session metadata
    conv.save_session_meta_data()
    
    # Delete from active sessions
    del active_sessions[user_id]
    
    return {"message": "Logged out successfully", "user_id": user_id}