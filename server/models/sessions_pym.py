from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionResponse(BaseModel):
    session_id: str
    user_id: str
    session_title: Optional[str] = None
    session_summary: Optional[str] = None
    created_at: datetime

class SessionMetadata(BaseModel):
    session_title: str
    session_summary: str