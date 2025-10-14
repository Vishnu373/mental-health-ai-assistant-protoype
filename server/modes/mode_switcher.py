from typing import Literal
from .database.user_profile_db import UserProfile as UserProfileDB, SessionLocal

def get_user_profile_data(user_id: str):
    db = SessionLocal()
    profile = db.query(UserProfileDB).filter(UserProfileDB.user_id == user_id).first()
    db.close()
    return profile

# getting manadatory fields/columns from database 
def get_mandatory_fields_from_db() -> list[str]:
    mandatory_fields = []
    
    for column in UserProfileDB.__table__.columns:
        if column.name not in ['user_id', 'session_id', 'created_at', 'updated_at'] and not column.nullable:
            mandatory_fields.append(column.name)
    
    return mandatory_fields

# Switching logic - if manadatory fields filled switch to therapy_mode else stay in info_collection_mode
def check_mandatory_fields_complete(profile: UserProfileDB) -> bool:
    if not profile:
        return False
    
    mandatory_fields = get_mandatory_fields_from_db()
    
    for field in mandatory_fields:
        field_value = getattr(profile, field, None)
        if (field_value is None or field_value == "" or field_value == "Not specified" or 
            field_value == 0 or field_value is False):
            return False
    
    return True

def determine_user_mode(user_id: str) -> Literal["info_collection", "therapy"]:
    profile = get_user_profile_data(user_id)
    
    if not profile:
        return "info_collection"
    
    if check_mandatory_fields_complete(profile):
        return "therapy"
    
    else:
        return "info_collection"

# Get detailed profile completion status for debugging/monitoring
def get_profile_completion_status(user_id: str) -> dict:
    profile = get_user_profile_data(user_id)
    
    if not profile:
        return {
            "user_id": user_id,
            "profile_exists": False,
            "mandatory_fields_complete": False,
            "current_mode": "info_collection",
            "ready_for_therapy": False,
            "mandatory_fields": get_mandatory_fields_from_db()
        }
    
    mandatory_complete = check_mandatory_fields_complete(profile)
    current_mode = "therapy" if mandatory_complete else "info_collection"
    
    return {
        "user_id": user_id,
        "profile_exists": True,
        "mandatory_fields_complete": mandatory_complete,
        "current_mode": current_mode,
        "ready_for_therapy": mandatory_complete,
        "mandatory_fields": get_mandatory_fields_from_db()
    }
