from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models.chats_pym import ChatResponse, ChatInput
from .services.chat_service import process_chat, get_chat_history
from datetime import datetime

app = FastAPI(title="Mental Health AI Assistant API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Mental Health AI Assistant API is running"}

@app.get("/ping")
def ping():
    return {
        "status": "alive", 
        "timestamp": datetime.now().isoformat(),
        "message": "Backend is running"
    }

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(chat_input: ChatInput):
    return process_chat(chat_input)

@app.get("/chat/history/{user_id}/{session_id}")
def get_history(user_id: str, session_id: str):
    return get_chat_history(user_id, session_id)
