from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone
import uuid
from urllib.parse import quote_plus

DB_USER = "postgres"
DB_PASSWORD = quote_plus("PostgresSQL123@")
DB_HOST = "127.0.0.1" 
DB_PORT = 5432
DB_NAME = "mhai"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(
    DATABASE_URL,
    connect_args={"host": DB_HOST}  # force TCP instead of socket
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User account related
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# Chat history for RAG context
class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String, index=True, default=lambda: str(uuid.uuid4()))
    user_query = Column(String, nullable=False)
    model_response = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# Create the table
Base.metadata.create_all(bind=engine)
