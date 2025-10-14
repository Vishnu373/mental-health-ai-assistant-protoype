from .models.chats_pym import ChatResponse, ChatInput
from .modes.info_collection_mode import info_collection_chat
from .modes.therapy_mode import therapy_chat
from .modes.mode_switcher import determine_user_mode
from .services.conversational import get_conversation_history

# Determine the mode by using the logic from mode_switcher.py
def process_chat(chat_input: ChatInput) -> ChatResponse:   
    # Determine which mode the user should be in
    user_mode = determine_user_mode(chat_input.user_id)
    
    if user_mode == "info_collection":
        response = info_collection_chat(
            user_id=chat_input.user_id,
            user_message=chat_input.query,
            session_id=chat_input.session_id
        )

    else:
        response = therapy_chat(
            user_id=chat_input.user_id,
            user_message=chat_input.query,
            session_id=chat_input.session_id
        )
    
    return response

# later use case
def get_chat_history(user_id: str, session_id: str) -> dict:
    history = get_conversation_history(user_id, session_id)
    return {
        "user_id": user_id,
        "session_id": session_id,
        "history": history
    }