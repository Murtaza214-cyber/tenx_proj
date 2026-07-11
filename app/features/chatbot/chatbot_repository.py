from sqlalchemy.orm import Session
from app.features.chatbot.chatbot_models import ChatMessage

class ChatbotRepository:
    @staticmethod
    def create_message(db: Session, role: str, content: str) -> ChatMessage:
        db_message = ChatMessage(role=role, content=content)
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    @staticmethod
    def get_chat_history(db: Session, limit: int = 50):
        return db.query(ChatMessage).order_by(ChatMessage.created_at.asc()).limit(limit).all()