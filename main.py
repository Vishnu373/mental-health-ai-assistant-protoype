from fastapi import FastAPI
from models.chats_pym import ChatResponse, ChatInput
from services.chat_service import process_chat, get_chat_history

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Mental Health AI Assistant API is running"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(chat_input: ChatInput):
    return process_chat(chat_input)

@app.get("/chat/history/{user_id}/{session_id}")
def get_history(user_id: str, session_id: str):
    return get_chat_history(user_id, session_id)
