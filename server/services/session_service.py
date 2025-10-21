import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict
from database.chats_db import Chat, SessionLocal as ChatSessionLocal
from database.user_profile_db import UserProfile as UserProfileDB, SessionLocal as ProfileSessionLocal
from services.conversational import generate_session_id, get_conversation_history
from modes.mode_switcher import get_mandatory_fields_from_db, check_mandatory_fields_complete

def get_or_create_user_session(user_id: str) -> Dict:
    db = ChatSessionLocal()
    
    try:
        latest_chat = db.query(Chat).filter(
            Chat.user_id == user_id
        ).order_by(Chat.created_at.desc()).first()
        
        if latest_chat:
            session_id = latest_chat.session_id
            recent_history = get_conversation_history(user_id, session_id, limit=10)
            
            return {
                "session_id": session_id,
                "is_new_session": False,
                "recent_history": recent_history,
                "message": "Continuing previous conversation"
            }
        else:
            session_id = generate_session_id()
            
            return {
                "session_id": session_id,
                "is_new_session": True,
                "recent_history": [],
                "message": "Starting new conversation"
            }
    
    finally:
        db.close()

def get_user_profile_status(user_id: str) -> Dict:
    db = ProfileSessionLocal()
    
    try:
        profile = db.query(UserProfileDB).filter(UserProfileDB.user_id == user_id).first()
        
        required_fields = get_mandatory_fields_from_db()
        
        if not profile:
            return {
                "profile_exists": False,
                "completed_fields": [],
                "missing_fields": required_fields,
                "completion_percentage": 0,
                "ready_for_therapy": False
            }
        
        completed_fields = []
        missing_fields = []
        
        is_profile_complete = check_mandatory_fields_complete(profile)
        
        for field in required_fields:
            value = getattr(profile, field, None)
            
            is_completed = not (
                value is None or 
                value == "" or 
                value == "Not specified" or 
                value == 0 or 
                value is False
            )
            
            if is_completed:
                completed_fields.append(field)
            else:
                missing_fields.append(field)
        
        completion_percentage = (len(completed_fields) / len(required_fields)) * 100 if required_fields else 100
        
        return {
            "profile_exists": True,
            "completed_fields": completed_fields,
            "missing_fields": missing_fields,
            "completion_percentage": completion_percentage,
            "ready_for_therapy": is_profile_complete
        }
    
    finally:
        db.close()

# Get comprehensive session context combining profile status and recent history.
def get_session_context(user_id: str, session_id: str) -> Dict:
    profile_status = get_user_profile_status(user_id)
    recent_history = get_conversation_history(user_id, session_id, limit=10)
    
    # Determine conversation state based on recent messages and missing fields
    conversation_state = "getting_started"
    if recent_history:
        missing_count = len(profile_status["missing_fields"])
        completed_count = len(profile_status["completed_fields"])
        
        if missing_count <= 2:
            conversation_state = "nearly_complete"
        elif completed_count > 3:
            conversation_state = "in_progress"
        else:
            conversation_state = "building_rapport"
    
    return {
        "user_id": user_id,
        "session_id": session_id,
        "profile_status": profile_status,
        "recent_history": recent_history,
        "conversation_state": conversation_state,
        "ready_for_therapy": profile_status["ready_for_therapy"]
    }