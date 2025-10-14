import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, Column, String, DateTime, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone
from urllib.parse import quote_plus
from server.config import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "user_profile"

    user_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, nullable=True, index=True)
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
    print("User profile table created successfully!")
