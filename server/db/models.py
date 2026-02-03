"""SQLAlchemy database models."""
from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone
from app.config import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Chat(Base):
    """Chat history table."""
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    user_message = Column(String, nullable=False)
    ai_response = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class SessionSummary(Base):
    """Session summary table for conversation context."""
    __tablename__ = "session_summaries"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    summary = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class UserProfile(Base):
    """User profile table."""
    __tablename__ = "user_profile"

    user_id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Mandatory fields
    age = Column(Integer, nullable=False)
    guardian_status = Column(String, nullable=False)
    upbringing_description = Column(String, nullable=False)
    cultural_background = Column(String, nullable=False)
    mental_health_conditions = Column(String, nullable=False)
    mental_health_medication = Column(String, nullable=False)
    mental_health_rating = Column(String, nullable=False)
    sleep_quality = Column(String, nullable=False)
    stress_frequency = Column(String, nullable=False)
    platform_goals = Column(String, nullable=False)
    therapist_matching_preference = Column(String, nullable=False)
    concern_contact_consent = Column(Boolean, nullable=False)
    data_consent = Column(Boolean, nullable=False)

    # Optional fields
    gender_identity = Column(String, nullable=True)
    relationship_status = Column(String, nullable=True)
    education_level = Column(String, nullable=True)
    employment_status = Column(String, nullable=True)
    institution_name = Column(String, nullable=True)
    program_major = Column(String, nullable=True)
    year_of_study = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    role_title = Column(String, nullable=True)
    years_in_workforce = Column(String, nullable=True)
    physical_activity_level = Column(String, nullable=True)
    ai_communication_style = Column(String, nullable=True)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")
