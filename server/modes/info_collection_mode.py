import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import re
from typing import List, Dict
from services.conversational import generate_session_id, chat_with_history
from services.session_service import get_session_context
from services.prompt_builder import remaining_information
from services.prompts import info_collection_prompt
from models.chats_pym import ChatInput, ChatResponse
from models.user_profile_pym import UserProfile
from database.user_profile_db import UserProfile as UserProfileDB, SessionLocal
from config import llm_model
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

def start_new_conversation() -> str:
    return generate_session_id()

# detection logic based on keywords for each fields
def detect_mentioned_fields(user_message: str) -> List[str]:
    field_names = list(UserProfile.model_fields.keys())
    
    field_keywords = {
        'age': ['years old', 'age', 'born in', 'i am', "i'm", 'turn', 'turning'],
        'employment_status': ['work', 'job', 'employed', 'student', 'unemployed', 'career', 'studying', 'working', 'freelance', 'retired', 'part-time', 'full-time', 'engineer', 'teacher', 'doctor', 'nurse'],
        'education_level': ['school', 'college', 'university', 'degree', 'study', 'graduate', 'undergraduate', 'postgraduate', 'masters', 'bachelor', 'phd', 'doctorate', 'high school'],
        'relationship_status': ['married', 'single', 'relationship', 'divorced', 'dating', 'partner', 'spouse', 'boyfriend', 'girlfriend', 'separated', 'widowed'],
        'mental_health_rating': ['feel', 'mental health', 'rate', 'scale', 'out of 10', '/10', 'rating', 'number'],
        'sleep_quality': ['sleep', 'sleeping', 'rest', 'tired', 'insomnia', 'wake up', 'bedtime', 'hours', 'well', 'poorly', 'good', 'bad', 'excellent', 'poor', 'fair'],
        'stress_frequency': ['stress', 'stressed', 'overwhelmed', 'anxious', 'pressure', 'daily', 'weekly', 'rarely', 'often', 'sometimes', 'always', 'never'],
        'guardian_status': ['parents', 'mom', 'dad', 'family', 'grew up', 'childhood', 'mother', 'father', 'divorced', 'married', 'single parent', 'raised by'],
        'upbringing_description': ['upbringing', 'childhood', 'family', 'grew up', 'stable', 'strict', 'supportive', 'chaotic', 'religious', 'distant', 'loving', 'harsh'],
        'platform_goals': ['want to', 'hope to', 'help with', 'goal', 'improve', 'manage', 'anxiety', 'depression', 'sleep', 'relationships', 'focus', 'trauma', 'lonely'],
        'data_consent': ['yes', 'consent', 'agree', 'okay', 'ok', 'sure', 'fine', 'no problem'],
        'gender_identity': ['male', 'female', 'man', 'woman', 'non-binary', 'transgender', 'genderqueer', 'prefer not'],
        'cultural_background': ['culture', 'ethnicity', 'background', 'heritage', 'race', 'nationality', 'from', 'born in'],
        'physical_activity_level': ['exercise', 'active', 'sedentary', 'gym', 'workout', 'sports', 'walking', 'running'],
        'ai_communication_style': ['formal', 'friendly', 'empathetic', 'direct', 'conversational', 'casual', 'professional']
    }
    
    mentioned_fields = []
    message_lower = user_message.lower()
    
    for field, keywords in field_keywords.items():
        if field in field_names and any(keyword in message_lower for keyword in keywords):
            mentioned_fields.append(field)
    
    return mentioned_fields

# Extract data from user response
def extract_field_data(user_message: str, detected_fields: List[str]) -> Dict:
    if not detected_fields:
        return {}
    
    extraction_prompt = f"""
    Extract ONLY these specific fields from the user message: {', '.join(detected_fields)}
    User message: "{user_message}"
    Return as JSON with only the fields that are clearly mentioned. Do not infer or assume.
    Example format:
    {{"age": 25, "employment_status": "Student"}}
    Return only the JSON, nothing else.
    """  
    
    parser = StrOutputParser()
    chain = llm_model | parser
    # Claude expects a conversation format with SystemMessage + HumanMessage
    messages = [
        SystemMessage(content=extraction_prompt),
        HumanMessage(content=user_message)
    ]
    extracted_text = chain.invoke(messages)
    
    if extracted_text.startswith('{') and extracted_text.endswith('}'):
        return json.loads(extracted_text)
    
    return {}

# Adding content to database
def update_user_profile(user_id: str, extracted_data: Dict):
    db = SessionLocal()
    profile = db.query(UserProfileDB).filter(UserProfileDB.user_id == user_id).first()
    
    if not profile:
        # Create new profile with 'Not specified' defaults (mode_switcher will recognize these as incomplete)
        profile = UserProfileDB(
            user_id=user_id,
            age=0,  # Special case: 0 will be treated as incomplete
            guardian_status="Not specified",
            upbringing_description="Not specified",
            cultural_background="Not specified",
            mental_health_conditions="Not specified",
            mental_health_medication="Not specified",
            mental_health_rating="Not specified",
            sleep_quality="Not specified",
            stress_frequency="Not specified",
            platform_goals="Not specified",
            therapist_matching_preference="Not specified",
            concern_contact_consent=False,  # False will be treated as incomplete
            data_consent=False
        )
        db.add(profile)
    
    # Define fields that need boolean conversion
    boolean_fields = ['data_consent', 'concern_contact_consent']
    
    for field, value in extracted_data.items():
        if hasattr(profile, field):
            # Convert string values to boolean for boolean fields
            if field in boolean_fields and isinstance(value, str):
                value = value.lower() in ['yes', 'true', '1', 'agree', 'consent']
            
            setattr(profile, field, value)
    
    db.commit()
    db.close()
    
    # For debugging or checking if it is getting stored in db
    print(f"Updated user {user_id} profile with: {extracted_data}")

# The pipeline for info_collection_mode
def info_collection_chat(user_id: str, user_message: str, session_id: str = None) -> ChatResponse:
    chat_input = ChatInput(
        query=user_message,
        user_id=user_id,
        session_id=session_id,
        model_name="claude-haiku-3.5"
    )
    
    # Get smart context (profile status + recent history)
    context = get_session_context(user_id, session_id)
    
    # Create enhanced prompt with context
    remaining_info_prompt = remaining_information(context)
    
    response = chat_with_history(user_id, chat_input, remaining_info_prompt)
    
    detected_fields = detect_mentioned_fields(user_message)
    
    if detected_fields:
        extracted_data = extract_field_data(user_message, detected_fields)
        if extracted_data:
            update_user_profile(user_id, extracted_data)
    
    return response
