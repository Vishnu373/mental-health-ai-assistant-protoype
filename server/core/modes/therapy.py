"""Therapy mode - provides therapeutic support using RAG."""
from db.schemas import ChatResponse
from core.rag.pipeline import retrieve, augment_and_generate
from services.session import get_conversation_history, generate_session_id, save_conversation_history
from core.modes.switcher import get_user_profile_data


def create_profile_based_query(user_profile) -> str:
    """Create retrieval query based on user's mental health conditions."""
    if user_profile and user_profile.mental_health_conditions:
        return user_profile.mental_health_conditions
    return "general mental health support"


def therapy_chat(user_id: str, user_message: str, session_id: str = None) -> ChatResponse:
    """Main therapy chat function using RAG pipeline."""
    if not session_id:
        session_id = generate_session_id()

    user_profile = get_user_profile_data(user_id)
    if not user_profile:
        return ChatResponse(
            response="I don't have enough information about you yet. Please complete the information collection first.",
            session_id=session_id,
            model_name="claude-haiku-3.5"
        )

    query = create_profile_based_query(user_profile)
    retrieved_content = retrieve(query)

    history = get_conversation_history(user_id, session_id)
    conversation_history = ""
    if history:
        conversation_history = "\n".join([f"User: {h[0]}\nTherapist: {h[1]}" for h in history[-3:]])

    ai_response = augment_and_generate(user_profile, retrieved_content, conversation_history, user_message)
    save_conversation_history(user_id, session_id, user_message, ai_response)

    return ChatResponse(response=ai_response, session_id=session_id, model_name="claude-haiku-3.5")
