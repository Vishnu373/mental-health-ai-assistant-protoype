from pydantic import BaseModel, EmailStr
from datetime import datetime

# User signing up
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# For logging in users
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Sending user info to API
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime


# Chatbot related
class ModelName:
    CLAUDE_HAIKU = "claude-haiku-3.5"

class ChatRequest(BaseModel):
    session_id: str
    query: str
    model_name: str = ModelName.CLAUDE_HAIKU

class ChatResponse(BaseModel):
    session_id: str
    query: str
    response: str
    model_name: str = ModelName.CLAUDE_HAIKU
