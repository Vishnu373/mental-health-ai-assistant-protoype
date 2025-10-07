from pydantic import BaseModel, Field
from typing import Optional

class UserProfile(BaseModel):
    age: int = Field(
        description="User's age in years"
    )
    gender_identity: Optional[str] = Field(
        default=None,
        description="Gender identity: Male, Female, Non-binary, Transgender, Genderqueer, Prefer not to say, Other"
    )
    relationship_status: Optional[str] = Field(
        default=None,
        description="Relationship status: Single, In a relationship, Married, Separated, Divorced, Widowed"
    )
    education_level: Optional[str] = Field(
        default=None,
        description="Education level: High school, Undergraduate, Graduate, Postgraduate, Other"
    )
    employment_status: Optional[str] = Field(
        default=None,
        description="Employment status: Student, Employed full-time, Employed part-time, Unemployed, Other"
    )
    institution_name: Optional[str] = Field(
        default=None,
        description="School/college name if student"
    )
    program_major: Optional[str] = Field(
        default=None,
        description="Study program or major if student"
    )
    year_of_study: Optional[str] = Field(
        default=None,
        description="Year of study if student"
    )
    industry: Optional[str] = Field(
        default=None,
        description="Industry field if employed"
    )
    role_title: Optional[str] = Field(
        default=None,
        description="Job title if employed"
    )
    years_in_workforce: Optional[str] = Field(
        default=None,
        description="Years of work experience if employed"
    )
    guardian_status: str = Field(
        description="Parent/Guardian status during upbringing: Married, Divorced, Single parent, Raised by others, Prefer not to say"
    )
    upbringing_description: str = Field(
        description="Description of upbringing: Stable, Strict, Emotionally distant, Supportive, Religious, Chaotic, Other"
    )
    cultural_background: str = Field(
        description="User's cultural background or ethnicity"
    )
    mental_health_conditions: str = Field(
        description="Any diagnosed mental health conditions (optional)"
    )
    mental_health_medication: str = Field(
        description="Any medication taken for mental health (optional)"
    )
    mental_health_rating: str = Field(
        description="Self-rated mental health on 1-10 scale"
    )
    physical_activity_level: Optional[str] = Field(
        default=None,
        description="Physical activity level: Sedentary, Lightly active, Moderately active, Very active"
    )
    sleep_quality: str = Field(
        description="Sleep quality: Poor, Fair, Good, Excellent"
    )
    stress_frequency: str = Field(
        description="How often feeling overwhelmed or stressed: Daily, Weekly, Rarely"
    )
    platform_goals: str = Field(
        description="What user hopes to get from platform: Manage anxiety, Improve focus, Deal with relationships, Heal from trauma, Sleep better, Explore thoughts safely, Feel less lonely, Other"
    )
    ai_communication_style: Optional[str] = Field(
        default=None,
        description="Preferred AI communication style: Formal, Friendly, Empathetic, Direct, Conversational"
    )
    therapist_matching_preference: str = Field(
        description="Preference for human therapist matching: Yes, No, Not sure yet"
    )
    concern_contact_consent: bool = Field(
        description="Consent to be contacted if concerning patterns detected: Yes, No"
    )
    data_consent: bool = Field(
        description="Consent to data collection, privacy practices, and terms of service: Yes, No"
    )