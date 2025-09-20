from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone
from database.config import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Chat history table
class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    user_message = Column(String, nullable=False)
    ai_response = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# Create the table
Base.metadata.create_all(bind=engine)