from sqlalchemy import create_engine, Column, String, DateTime, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone
from urllib.parse import quote_plus
from database.config import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "user_profile"

    user_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    age = Column(Integer, nullable=True)
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
    
    guardian_status = Column(String, nullable=True)
    upbringing_description = Column(String, nullable=True)
    cultural_background = Column(String, nullable=True)
    
    mental_health_conditions = Column(String, nullable=True)
    mental_health_medication = Column(String, nullable=True)
    mental_health_rating = Column(String, nullable=True)
    physical_activity_level = Column(String, nullable=True)
    sleep_quality = Column(String, nullable=True)
    stress_frequency = Column(String, nullable=True)
    
    platform_goals = Column(String, nullable=True)
    ai_communication_style = Column(String, nullable=True)
    therapist_matching_preference = Column(String, nullable=True)
    
    concern_contact_consent = Column(Boolean, nullable=True)
    data_consent = Column(Boolean, nullable=True)

# Create the table
Base.metadata.create_all(bind=engine)