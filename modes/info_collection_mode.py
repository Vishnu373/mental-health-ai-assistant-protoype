import json
from typing import List, Dict
from services.conversational import generate_session_id, chat_with_history
from services.prompts import info_collection_prompt
from models.chats_pym import ChatInput, ChatResponse
from models.user_profile_pym import UserProfile
from database.user_profile_db import UserProfile as UserProfileDB, SessionLocal
from rag.config import llm_model
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

def start_new_conversation() -> str:
    return generate_session_id()

# detection logic based on keywords for each fields
def detect_mentioned_fields(user_message: str) -> List[str]:
    field_names = list(UserProfile.model_fields.keys())
    
    field_keywords = {
        'age': ['years old', 'age', 'born in', 'i am', 'i\'m'],
        'employment_status': ['work', 'job', 'employed', 'student', 'unemployed', 'career'],
        'education_level': ['school', 'college', 'university', 'degree', 'study', 'graduate'],
        'relationship_status': ['married', 'single', 'relationship', 'divorced', 'dating'],
        'mental_health_rating': ['feel', 'mental health', 'rate', 'scale', 'out of 10'],
        'sleep_quality': ['sleep', 'sleeping', 'rest', 'tired', 'insomnia'],
        'stress_frequency': ['stress', 'stressed', 'overwhelmed', 'anxious', 'pressure'],
        'guardian_status': ['parents', 'mom', 'dad', 'family', 'grew up', 'childhood'],
        'upbringing_description': ['upbringing', 'childhood', 'family', 'grew up'],
        'platform_goals': ['want to', 'hope to', 'help with', 'goal', 'improve', 'manage'],
        'data_consent': ['yes', 'consent', 'agree', 'okay', 'ok']
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
        profile = UserProfileDB(user_id=user_id)
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
    
    response = chat_with_history(user_id, chat_input, info_collection_prompt)
    
    detected_fields = detect_mentioned_fields(user_message)
    
    if detected_fields:
        extracted_data = extract_field_data(user_message, detected_fields)
        if extracted_data:
            update_user_profile(user_id, extracted_data)
    
    return response
