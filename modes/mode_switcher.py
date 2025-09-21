from database.user_profile_db import UserProfile as UserProfileDB, SessionLocal

def get_user_profile_data(user_id: str):
    db = SessionLocal()
    profile = db.query(UserProfileDB).filter(UserProfileDB.user_id == user_id).first()
    db.close()
    
    return profile