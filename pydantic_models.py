# Defining the schema
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class ModelName(str, Enum):
    ClAUDE_HAIKU = "us.anthropic.claude-3-5-haiku-20241022-v1:0"

class QueryInput(BaseModel):
    question: str
    session_id: str | None = None
    model: ModelName = ModelName.CLAUDE_HAIKU

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName