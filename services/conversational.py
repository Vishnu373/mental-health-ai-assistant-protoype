import uuid
from typing import List
from datetime import datetime, timezone
from database.chats_db import Chat, SessionLocal
from models.chats_pym import ChatInput, ChatResponse
from config import llm_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    
def generate_session_id() -> str:
    return str(uuid.uuid4())

def get_conversation_history(user_id: str, session_id: str, limit: int = 10) -> List[tuple]:
    db = SessionLocal()
    
    chats = db.query(Chat).filter(
        Chat.user_id == user_id,
        Chat.session_id == session_id
    ).order_by(Chat.created_at.desc()).limit(limit).all()
    
    conversation_history = []
    for chat in reversed(chats):
        conversation_history.append((chat.user_message, chat.ai_response))
    
    db.close()
    return conversation_history

def save_conversation_history(user_id: str, session_id: str, user_message: str, ai_response: str):
    db = SessionLocal()
    
    chat = Chat(
        user_id=user_id,
        session_id=session_id,
        user_message=user_message,
        ai_response=ai_response,
        created_at=datetime.now(timezone.utc)
    )
    
    db.add(chat)
    db.commit()
    db.close()

def chat_with_history(user_id: str, chat_input: ChatInput, content_mode) -> ChatResponse:
    # 0. get the session id (exisiting user) or generate session id(new user) 
    session_id = chat_input.session_id or generate_session_id()
    
    # 1. get the history
    history = get_conversation_history(user_id, session_id)
    
    messages = []
    
    # 2. AI behaviour
    system_message = SystemMessage(content=content_mode)
    messages.append(system_message)
    
    # 3. combining response with history if it exists
    if history:
        for user_msg, ai_msg in history:
            messages.append(HumanMessage(content=user_msg))
            messages.append(AIMessage(content=ai_msg))
    
    # 4. Formats response as user_message and ai_reponse for storing it in messages[]
    user_message = HumanMessage(content=chat_input.query)
    messages.append(user_message)
    
    response = llm_model.invoke(messages)
    ai_response = response.content
    
    # 5. saves the conversation
    save_conversation_history(user_id, session_id, chat_input.query, ai_response)
    
    return ChatResponse(
        response=ai_response,
        session_id=session_id,
        model_name=chat_input.model_name
    )