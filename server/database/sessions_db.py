import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone
from config import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Sessions(Base):
    __tablename__ = "sessions"
    session_id = Column(String, primary_key=True, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    session_title = Column(String, nullable=True)
    session_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime(timezone=True), nullable=True)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Sessions table created successfully!")
