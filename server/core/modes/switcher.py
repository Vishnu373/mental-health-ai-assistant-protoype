"""Mode switcher - determines which mode user should be in."""
from typing import Literal
from core.fields import get_unfilled_fields, is_returning_user, get_filled_fields_count
from db.models import UserProfile as UserProfileDB, SessionLocal


def get_user_profile_data(user_id: str):
    """Get user profile from database."""
    db = SessionLocal()
    try:
        return db.query(UserProfileDB).filter(UserProfileDB.user_id == user_id).first()
    finally:
        db.close()


def determine_user_mode(user_id: str) -> Literal["info_collection", "therapy"]:
    """Determine which mode user should be in based on profile completion."""
    if not is_returning_user(user_id):
        return "info_collection"

    unfilled_required = get_unfilled_fields(user_id, required_only=True)
    return "therapy" if len(unfilled_required) == 0 else "info_collection"


def get_profile_completion_status(user_id: str) -> dict:
    """Get profile completion status for debugging/frontend."""
    profile_exists = is_returning_user(user_id)

    if not profile_exists:
        return {
            "user_id": user_id,
            "profile_exists": False,
            "mandatory_fields_complete": False,
            "current_mode": "info_collection",
            "ready_for_therapy": False,
            "completion_stats": get_filled_fields_count(user_id)
        }

    unfilled_required = get_unfilled_fields(user_id, required_only=True)
    mandatory_complete = len(unfilled_required) == 0

    return {
        "user_id": user_id,
        "profile_exists": True,
        "mandatory_fields_complete": mandatory_complete,
        "current_mode": "therapy" if mandatory_complete else "info_collection",
        "ready_for_therapy": mandatory_complete,
        "unfilled_fields": [f["name"] for f in unfilled_required],
        "completion_stats": get_filled_fields_count(user_id)
    }
