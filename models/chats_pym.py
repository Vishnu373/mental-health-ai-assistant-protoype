from pydantic import BaseModel, Field
from typing import Optional

class ModelName:
    CLAUDE_HAIKU = "claude-haiku-3.5"

class ChatInput(BaseModel):
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    model_name: str = ModelName.CLAUDE_HAIKU

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None
    model_name: str = ModelName.CLAUDE_HAIKU
