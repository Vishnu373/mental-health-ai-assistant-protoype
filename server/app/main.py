import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from typing import List, Dict
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.schemas import ChatResponse, ChatInput
from db.models import Chat, SessionSummary, SessionLocal
from app.config import llm_model
from core.modes.info_collection import info_collection_chat
# from core.modes.therapy import therapy_chat
from core.modes.switcher import determine_user_mode, get_profile_completion_status
from langchain_core.messages import SystemMessage, HumanMessage

app = FastAPI(title="Mental Health AI Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# HEALTH & MONITORING
# ============================================================================

@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "Mental Health AI Assistant API is running"}


@app.get("/ping")
def ping():
    """Ping endpoint for monitoring."""
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat(),
        "message": "Backend is running"
    }


# ============================================================================
# CHAT ENDPOINTS
# ============================================================================

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(chat_input: ChatInput):
    """Process a chat message."""
    user_mode = determine_user_mode(chat_input.user_id)

    if user_mode == "info_collection":
        return info_collection_chat(
            user_id=chat_input.user_id,
            user_message=chat_input.query,
            session_id=chat_input.session_id
        )
    else:
        return therapy_chat(
            user_id=chat_input.user_id,
            user_message=chat_input.query,
            session_id=chat_input.session_id
        )


@app.get("/chat/history/{user_id}/{session_id}")
def get_history(user_id: str, session_id: str):
    """Get chat history for a session."""
    db = SessionLocal()
    try:
        chats = db.query(Chat).filter(
            Chat.user_id == user_id,
            Chat.session_id == session_id
        ).order_by(Chat.created_at.desc()).limit(50).all()
        history = [(chat.user_message, chat.ai_response) for chat in reversed(chats)]
        return {"user_id": user_id, "session_id": session_id, "history": history}
    finally:
        db.close()


# ============================================================================
# SESSION ENDPOINTS
# ============================================================================

def generate_session_id() -> str:
    """Generate a new session ID."""
    return str(uuid.uuid4())


@app.get("/session/{user_id}")
def get_user_session(user_id: str):
    """Get or create a session for a user."""
    db = SessionLocal()
    try:
        latest_chat = db.query(Chat).filter(
            Chat.user_id == user_id
        ).order_by(Chat.created_at.desc()).first()

        if latest_chat:
            session_id = latest_chat.session_id
            chats = db.query(Chat).filter(
                Chat.user_id == user_id,
                Chat.session_id == session_id
            ).order_by(Chat.created_at.desc()).limit(10).all()
            recent_history = [(c.user_message, c.ai_response) for c in reversed(chats)]
            return {
                "session_id": session_id,
                "is_new_session": False,
                "is_returning_user": True,
                "recent_history": recent_history,
                "message": "Continuing previous conversation"
            }
        else:
            return {
                "session_id": generate_session_id(),
                "is_new_session": True,
                "is_returning_user": False,
                "recent_history": [],
                "message": "Starting new conversation"
            }
    finally:
        db.close()


@app.post("/session/end/{user_id}/{session_id}")
def end_session(user_id: str, session_id: str):
    """End session and save conversation summary."""
    db = SessionLocal()
    try:
        chats = db.query(Chat).filter(
            Chat.user_id == user_id,
            Chat.session_id == session_id
        ).order_by(Chat.created_at.asc()).limit(50).all()

        if not chats:
            return {"message": "No conversation to summarize", "summary_saved": False}

        history_text = "\n".join([f"User: {c.user_message}\nAI: {c.ai_response}" for c in chats])

        summary_prompt = """Summarize this conversation focusing on:
- Personal information shared
- Emotional state and concerns
- Key topics discussed
Keep it concise (2-3 paragraphs). Write in third person."""

        messages = [
            SystemMessage(content=summary_prompt),
            HumanMessage(content=f"Conversation:\n\n{history_text}")
        ]
        summary = llm_model.invoke(messages).content

        existing = db.query(SessionSummary).filter(
            SessionSummary.user_id == user_id,
            SessionSummary.session_id == session_id
        ).first()

        if existing:
            existing.summary = summary
            existing.created_at = datetime.now(timezone.utc)
        else:
            db.add(SessionSummary(
                user_id=user_id,
                session_id=session_id,
                summary=summary,
                created_at=datetime.now(timezone.utc)
            ))
        db.commit()
        return {"message": "Session ended", "summary_saved": True}
    finally:
        db.close()


# ============================================================================
# PROFILE ENDPOINTS
# ============================================================================

@app.get("/profile/status/{user_id}")
def get_profile_status(user_id: str):
    """Get profile completion status for frontend context indicator."""
    return get_profile_completion_status(user_id)
