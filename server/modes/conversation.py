import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from database.sessions_db import Sessions, SessionLocal
from database.chats_db import Chat
from config import llm_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from prompts.base_prompts import SESSION_METADATA_PROMPT

class Conversation:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.session_id = None
    
    def is_returning_user(self) -> bool:
        """Return True if user has any prior sessions."""
        db = SessionLocal()
        try:
            exists = db.query(Sessions.session_id).filter(
                Sessions.user_id == self.user_id
            ).first()
            return exists is not None
        finally:
            db.close()
    
    def get_last_session_summary(self) -> Optional[str]:
        """Return the most recent non-empty session_summary for the user, if any."""
        db = SessionLocal()
        try:
            last = db.query(Sessions).filter(
                Sessions.user_id == self.user_id,
                Sessions.session_summary != None  # noqa: E711 (intentional SQL None)
            ).order_by(Sessions.created_at.desc()).first()
            return last.session_summary if last else None
        finally:
            db.close()
    
    def get_conversation_history(self, limit: int = 10) -> List[tuple]:
        """Get conversation history for current session"""
        if not self.session_id:
            return []
        
        db = SessionLocal()
        try:
            chats = db.query(Chat).filter(
                Chat.user_id == self.user_id,
                Chat.session_id == self.session_id
            ).order_by(Chat.created_at.desc()).limit(limit).all()
            
            conversation_history = []
            for chat in reversed(chats):
                conversation_history.append((chat.user_message, chat.ai_response))
            
            return conversation_history
        finally:
            db.close()
    
    def save_conversation_history(self, user_message: str, ai_response: str):
        """Save conversation to database"""
        db = SessionLocal()
        try:
            chat = Chat(
                user_id=self.user_id,
                session_id=self.session_id,
                user_message=user_message,
                ai_response=ai_response,
                created_at=datetime.now(timezone.utc)
            )
            db.add(chat)
            db.commit()
        finally:
            db.close()
    
    def start_session(self) -> str:
        """Generate new session_id and store in database"""
        self.session_id = str(uuid.uuid4())
        
        db = SessionLocal()
        try:
            new_session = Sessions(
                session_id=self.session_id,
                user_id=self.user_id,
                created_at=datetime.now(timezone.utc)
            )
            db.add(new_session)
            db.commit()
        finally:
            db.close()
        
        return self.session_id
    
    def chat(self, user_message: str, content_mode: str) -> str:
        """Handle conversation with AI and store in history"""
        if not self.session_id:
            raise ValueError("Session not started. Call start_session() first.")
        
        history = self.get_conversation_history()
        
        messages = []
        messages.append(SystemMessage(content=content_mode))
        
        if history:
            for user_msg, ai_msg in history:
                messages.append(HumanMessage(content=user_msg))
                messages.append(AIMessage(content=ai_msg))
        
        messages.append(HumanMessage(content=user_message))
        
        response = llm_model.invoke(messages)
        ai_response = response.content
        
        self.save_conversation_history(user_message, ai_response)
        
        return ai_response
    
    def generate_session_metadata(self) -> Dict[str, str]:
        """Generate session title and summary using LLM"""
        if not self.session_id:
            raise ValueError("Session not started. Call start_session() first.")
        
        history = self.get_conversation_history()
        
        if not history:
            return {
                "session_title": "New Session",
                "session_summary": "No conversation yet."
            }
        
        conversation_text = "\n".join([
            f"User: {user_msg}\nAI: {ai_msg}" 
            for user_msg, ai_msg in history
        ])
        
        prompt = SESSION_METADATA_PROMPT.format(conversation=conversation_text)
        
        messages = [HumanMessage(content=prompt)]
        response = llm_model.invoke(messages)
        
        response_text = response.content
        title = "New Session"
        summary = "Conversation completed."
        
        if "Title:" in response_text and "Summary:" in response_text:
            parts = response_text.split("Summary:")
            title = parts[0].replace("Title:", "").strip()
            summary = parts[1].strip()
        
        return {
            "session_title": title,
            "session_summary": summary
        }
    
    def save_session_meta_data(self):
        """Generate metadata and update session in database"""
        if not self.session_id:
            raise ValueError("Session not started. Call start_session() first.")
        
        metadata = self.generate_session_metadata()
        
        db = SessionLocal()
        try:
            session = db.query(Sessions).filter(
                Sessions.session_id == self.session_id
            ).first()
            
            if session:
                session.session_title = metadata["session_title"]
                session.session_summary = metadata["session_summary"]
                session.ended_at = datetime.now(timezone.utc)
                db.commit()
        finally:
            db.close()
    
