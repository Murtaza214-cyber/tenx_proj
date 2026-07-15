# app/features/chatbot/chatbot_models.py
from typing import Literal
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from pydantic import BaseModel, Field
from app.config.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)     # 'user' or 'model'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String, nullable=True)  # 🔑 Tracks individual conversation threads

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatPayload(BaseModel):
    session_id: str
    message: str
    cache_mode: Literal["exact", "semantic", "disabled"] = Field(default="semantic")