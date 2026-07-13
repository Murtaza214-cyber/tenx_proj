from sqlalchemy.orm import Session
from app.features.chatbot.chatbot_models import ChatMessage

class ChatbotRepository:
    @staticmethod
    def create_message(db: Session, role: str, content: str, session_id: str = None):
        """
        Saves a message bound to its unique conversation session thread.
        Default session_id is None to avoid breaking older data entries.
        """
        new_msg = ChatMessage(
            role=role, 
            content=content, 
            session_id=session_id
        )
        db.add(new_msg)
        db.commit()
        db.refresh(new_msg)
        return new_msg

    @staticmethod
    def get_chat_history(db: Session, limit: int = 50):
        return db.query(ChatMessage).order_by(ChatMessage.created_at.asc()).limit(limit).all()
    
    @staticmethod
    def get_session_history(db: Session, session_id: str, limit: int = 50):
        return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).limit(limit).all()
    

    