"""Info collection mode - collects user profile data through conversation."""
import json
from typing import Optional
from core.fields import (
    get_next_unfilled_field,
    is_returning_user,
    get_filled_fields_count,
    get_unfilled_fields
)
from core.summary import get_latest_summary
from core.session import get_conversation_history, save_conversation_history, generate_session_id
from db.schemas import ChatInput, ChatResponse
from db.models import UserProfile as UserProfileDB, SessionLocal
from app.config import llm_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser


def get_or_create_profile(user_id: str) -> UserProfileDB:
    """Get existing profile or create a new one with defaults."""
    db = SessionLocal()
    try:
        profile = db.query(UserProfileDB).filter(UserProfileDB.user_id == user_id).first()
        if not profile:
            profile = UserProfileDB(
                user_id=user_id,
                age=0,
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
                concern_contact_consent=False,
                data_consent=False
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
        return profile
    finally:
        db.close()


def build_collection_prompt(next_field: dict | None, conversation_summary: str, recent_history: list, is_new_user: bool) -> str:
    """Build the system prompt for info collection."""
    history_text = ""
    if recent_history:
        for user_msg, ai_msg in recent_history[-5:]:
            history_text += f"User: {user_msg}\nAI: {ai_msg}\n"

    if is_new_user and (not next_field or next_field["name"] == "data_consent"):
        return f"""You are a warm, friendly AI companion starting a conversation with a new user.

**YOUR FIRST MESSAGE MUST:**
1. Warmly greet the user
2. Briefly explain you're here to provide personalized mental health support
3. Ask for their consent to collect personal information
4. Wait for them to agree before proceeding

Keep it SHORT (2-3 sentences). Do NOT mention data collection clinically.

**RECENT CONVERSATION:**
{history_text if history_text else "No conversation yet."}"""

    field_instruction = ""
    if next_field:
        field_instruction = f"""
**CURRENT FIELD TO COLLECT:**
Field: {next_field["name"]}
Description: {next_field["description"]}

Ask about this naturally. One question at a time."""
    else:
        field_instruction = "**ALL REQUIRED FIELDS COLLECTED!** Continue friendly conversation."

    summary_section = f"**PREVIOUS SESSION CONTEXT:**\n{conversation_summary}\n" if conversation_summary else ""

    return f"""You are a warm, empathetic AI companion.

{summary_section}{field_instruction}

**RECENT CONVERSATION:**
{history_text if history_text else "Starting fresh."}

**GUIDELINES:**
- Keep responses SHORT (1-2 sentences)
- Be friendly, not clinical
- Do NOT mention data collection
- Acknowledge what they share before asking next thing"""


def extract_field_value(user_message: str, field: dict) -> Optional[str]:
    """Extract and validate field value against the field description."""
    extraction_prompt = f"""Analyze if the user's message contains a valid answer for this field.

FIELD: {field["name"]}
DESCRIPTION: {field["description"]}
USER MESSAGE: "{user_message}"

TASK:
1. Check if the user's message contains information relevant to "{field["name"]}"
2. If YES and the value makes sense for "{field["description"]}", extract it
3. If NO (user is asking questions, talking about other topics, or answer doesn't match the field), return SKIP

EXAMPLES:
- Field: age, User says "I'm 25 years old" → Return: 25
- Field: age, User says "What do you mean?" → Return: SKIP  
- Field: sleep_quality, User says "I sleep well" → Return: good
- Field: sleep_quality, User says "Tell me about yourself" → Return: SKIP
- Field: data_consent, User says "Yes I agree" → Return: true
- Field: data_consent, User says "What data?" → Return: SKIP

Return ONLY the extracted value OR the word SKIP:"""

    messages = [SystemMessage(content=extraction_prompt), HumanMessage(content=user_message)]
    parser = StrOutputParser()
    result = (llm_model | parser).invoke(messages).strip()
    
    if not result or result.upper() == "SKIP" or len(result) > 150:
        return None
    return result


def update_user_profile(user_id: str, field_name: str, value: str):
    """Update a single field in the user profile."""
    db = SessionLocal()
    try:
        profile = db.query(UserProfileDB).filter(UserProfileDB.user_id == user_id).first()
        if not profile:
            return

        if field_name == "age":
            try:
                value = int(value)
            except ValueError:
                return
        elif field_name in ["data_consent", "concern_contact_consent"]:
            value = value.lower() in ["true", "yes", "agree", "consent", "1"]

        if hasattr(profile, field_name):
            setattr(profile, field_name, value)
            db.commit()
    finally:
        db.close()


def info_collection_chat(user_id: str, user_message: str, session_id: str = None) -> ChatResponse:
    """Main info collection chat function."""
    if not session_id:
        session_id = generate_session_id()

    get_or_create_profile(user_id)
    returning = is_returning_user(user_id)
    is_new_user = not returning

    conversation_summary = get_latest_summary(user_id) if returning else ""
    next_field = get_next_unfilled_field(user_id)
    recent_history = get_conversation_history(user_id, session_id, limit=10)

    system_prompt = build_collection_prompt(
        next_field=next_field,
        conversation_summary=conversation_summary,
        recent_history=recent_history,
        is_new_user=is_new_user and len(recent_history) == 0
    )

    messages = [SystemMessage(content=system_prompt)]
    for user_msg, ai_msg in recent_history:
        messages.append(HumanMessage(content=user_msg))
        messages.append(AIMessage(content=ai_msg))
    messages.append(HumanMessage(content=user_message))

    ai_response = llm_model.invoke(messages).content

    if next_field:
        extracted = extract_field_value(user_message, next_field)
        if extracted:
            update_user_profile(user_id, next_field["name"], extracted)

    save_conversation_history(user_id, session_id, user_message, ai_response)

    return ChatResponse(response=ai_response, session_id=session_id, model_name="claude-haiku-3.5")
