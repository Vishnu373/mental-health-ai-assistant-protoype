"""Summary utilities - internal helpers for conversation context."""
from db.models import SessionSummary, SessionLocal


def get_latest_summary(user_id: str) -> str:
    """Get most recent conversation summary for a user."""
    db = SessionLocal()
    try:
        latest = db.query(SessionSummary).filter(
            SessionSummary.user_id == user_id
        ).order_by(SessionSummary.created_at.desc()).first()
        return latest.summary if latest else ""
    finally:
        db.close()
