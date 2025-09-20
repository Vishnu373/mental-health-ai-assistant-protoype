from models.chats_pym import ChatResponse, ChatInput
from modes.info_collection_mode import info_collection_chat
from services.conversational import get_conversation_history

"""Process chat request - uses info_collection_mode pipeline"""
def process_chat(chat_input: ChatInput) -> ChatResponse:
    response = info_collection_chat(
        user_id=chat_input.user_id,
        user_message=chat_input.query,
        session_id=chat_input.session_id
    )

    return response

"""Get chat history for a user session
For later purpose
"""
def get_chat_history(user_id: str, session_id: str) -> dict:
    history = get_conversation_history(user_id, session_id)
    return {
        "user_id": user_id,
        "session_id": session_id,
        "history": history
    }