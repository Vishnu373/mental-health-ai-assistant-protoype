"""Pydantic schemas for API validation."""
from pydantic import BaseModel, Field
from typing import Optional


class ModelName:
    CLAUDE_HAIKU = "claude-haiku-3.5"


class ChatInput(BaseModel):
    """Input schema for chat endpoint."""
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    model_name: str = ModelName.CLAUDE_HAIKU


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    response: str
    session_id: Optional[str] = None
    model_name: str = ModelName.CLAUDE_HAIKU


class UserProfileSchema(BaseModel):
    """User profile schema for validation."""
    age: int = Field(description="User's age in years")
    gender_identity: Optional[str] = Field(default=None, description="Gender identity")
    relationship_status: Optional[str] = Field(default=None, description="Relationship status")
    education_level: Optional[str] = Field(default=None, description="Education level")
    employment_status: Optional[str] = Field(default=None, description="Employment status")
    institution_name: Optional[str] = Field(default=None, description="School/college name if student")
    program_major: Optional[str] = Field(default=None, description="Study program or major")
    year_of_study: Optional[str] = Field(default=None, description="Year of study")
    industry: Optional[str] = Field(default=None, description="Industry field if employed")
    role_title: Optional[str] = Field(default=None, description="Job title if employed")
    years_in_workforce: Optional[str] = Field(default=None, description="Years of work experience")
    guardian_status: str = Field(description="Parent/Guardian status during upbringing")
    upbringing_description: str = Field(description="Description of upbringing")
    cultural_background: str = Field(description="User's cultural background")
    mental_health_conditions: str = Field(description="Diagnosed mental health conditions")
    mental_health_medication: str = Field(description="Medication for mental health")
    mental_health_rating: str = Field(description="Self-rated mental health 1-10")
    physical_activity_level: Optional[str] = Field(default=None, description="Physical activity level")
    sleep_quality: str = Field(description="Sleep quality")
    stress_frequency: str = Field(description="How often feeling overwhelmed")
    platform_goals: str = Field(description="What user hopes to get from platform")
    ai_communication_style: Optional[str] = Field(default=None, description="Preferred AI communication style")
    therapist_matching_preference: str = Field(description="Preference for human therapist matching")
    concern_contact_consent: bool = Field(description="Consent to be contacted if concerning patterns")
    data_consent: bool = Field(description="Consent to data collection")
