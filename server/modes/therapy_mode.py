from models.chats_pym import ChatInput, ChatResponse
from rag.rag_pipeline import retrieve, augment_and_generate
from services.conversational import get_conversation_history, generate_session_id, save_conversation_history
from modes.mode_switcher import get_user_profile_data

# Create retrieval query based on user's mental health conditions
def create_profile_based_query(user_profile):
    if user_profile and user_profile.mental_health_conditions:
        return user_profile.mental_health_conditions
    
    else:
        return "general mental health support"

# therapy mode pipeline
def therapy_chat(user_id: str, user_message: str, session_id: str = None) -> ChatResponse:    
    # 1. Get or generate session ID
    if not session_id:
        session_id = generate_session_id()
    
    # 2. Get user profile from database
    user_profile = get_user_profile_data(user_id)
    
    if not user_profile:
        return ChatResponse(
            response="I don't have enough information about you yet to provide personalized therapy. Please complete the information collection first.",
            session_id=session_id,
            model_name="claude-haiku-3.5"
        )
    
    # 3. Create retrieval query based on mental health conditions
    query = create_profile_based_query(user_profile)
    
    # 4. Retrieve relevant therapeutic content
    retrieved_content = retrieve(query)
    
    # 5. Get conversation history for context
    history = get_conversation_history(user_id, session_id)
    conversation_history = ""
    if history:
        conversation_history = "\n".join([f"User: {h[0]}\nTherapist: {h[1]}" for h in history[-3:]])  # Last 3 exchanges
    
    # 6. Augment and generate therapeutic response
    ai_response = augment_and_generate(user_profile, retrieved_content, conversation_history, user_message)
    
    # 7. Save conversation to history
    save_conversation_history(user_id, session_id, user_message, ai_response)
    
    # 8. Return response
    return ChatResponse(
        response=ai_response,
        session_id=session_id,
        model_name="claude-haiku-3.5"
    )