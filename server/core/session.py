"""Session utilities - internal helpers for conversation management."""
import uuid
from typing import List
from datetime import datetime, timezone
from db.models import Chat, SessionLocal


def generate_session_id() -> str:
    """Generate a new session ID."""
    return str(uuid.uuid4())


def get_conversation_history(user_id: str, session_id: str, limit: int = 10) -> List[tuple]:
    """Get conversation history for a session."""
    db = SessionLocal()
    try:
        chats = db.query(Chat).filter(
            Chat.user_id == user_id,
            Chat.session_id == session_id
        ).order_by(Chat.created_at.desc()).limit(limit).all()
        return [(chat.user_message, chat.ai_response) for chat in reversed(chats)]
    finally:
        db.close()


def save_conversation_history(user_id: str, session_id: str, user_message: str, ai_response: str):
    """Save a conversation exchange."""
    db = SessionLocal()
    try:
        chat = Chat(
            user_id=user_id,
            session_id=session_id,
            user_message=user_message,
            ai_response=ai_response,
            created_at=datetime.now(timezone.utc)
        )
        db.add(chat)
        db.commit()
    finally:
        db.close()
