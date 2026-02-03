"""Field service - dynamic field detection using Pydantic schema."""
from typing import Optional
from db.schemas import UserProfileSchema
from db.models import UserProfile as UserProfileDB, SessionLocal


def get_all_fields_with_metadata() -> list[dict]:
    """Get all fields from UserProfileSchema with their metadata."""
    fields = []
    for name, field_info in UserProfileSchema.model_fields.items():
        fields.append({
            "name": name,
            "description": field_info.description or f"User's {name.replace('_', ' ')}",
            "is_required": field_info.is_required(),
            "field_type": str(field_info.annotation) if field_info.annotation else "str"
        })
    return fields


def get_required_fields() -> list[dict]:
    """Get only required fields."""
    return [f for f in get_all_fields_with_metadata() if f["is_required"]]


def get_optional_fields() -> list[dict]:
    """Get only optional fields."""
    return [f for f in get_all_fields_with_metadata() if not f["is_required"]]


def is_returning_user(user_id: str) -> bool:
    """Check if user_id exists in database (Clerk ID lookup)."""
    db = SessionLocal()
    try:
        return db.query(UserProfileDB).filter(UserProfileDB.user_id == user_id).first() is not None
    finally:
        db.close()


def get_user_profile_as_dict(user_id: str) -> dict | None:
    """Get user profile as dictionary."""
    db = SessionLocal()
    try:
        profile = db.query(UserProfileDB).filter(UserProfileDB.user_id == user_id).first()
        if not profile:
            return None
        return {c.name: getattr(profile, c.name) for c in profile.__table__.columns}
    finally:
        db.close()


def get_unfilled_fields(user_id: str, required_only: bool = True) -> list[dict]:
    """Get fields that still need to be filled for this user."""
    profile_data = get_user_profile_as_dict(user_id)
    all_fields = get_required_fields() if required_only else get_all_fields_with_metadata()

    if not profile_data:
        return all_fields

    unfilled = []
    for field in all_fields:
        field_name = field["name"]
        value = profile_data.get(field_name)
        is_empty = (
            value is None or value == "" or value == "Not specified" or
            (field_name not in ["concern_contact_consent", "data_consent"] and value == 0) or
            (field_name in ["concern_contact_consent", "data_consent"] and value is False)
        )
        if is_empty:
            unfilled.append(field)

    return unfilled


def get_next_unfilled_field(user_id: str) -> dict | None:
    """Get the next field that needs to be filled."""
    unfilled_required = get_unfilled_fields(user_id, required_only=True)
    if unfilled_required:
        return unfilled_required[0]

    unfilled_optional = get_unfilled_fields(user_id, required_only=False)
    return unfilled_optional[0] if unfilled_optional else None


def get_filled_fields_count(user_id: str) -> dict:
    """Get count of filled vs total fields for progress tracking."""
    all_fields = get_all_fields_with_metadata()
    required_fields = get_required_fields()
    unfilled_all = get_unfilled_fields(user_id, required_only=False)
    unfilled_required = get_unfilled_fields(user_id, required_only=True)

    return {
        "total_fields": len(all_fields),
        "filled_fields": len(all_fields) - len(unfilled_all),
        "required_total": len(required_fields),
        "required_filled": len(required_fields) - len(unfilled_required),
        "completion_percentage": round(
            ((len(required_fields) - len(unfilled_required)) / len(required_fields)) * 100
            if required_fields else 100, 1
        )
    }
