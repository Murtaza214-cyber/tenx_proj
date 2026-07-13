# app/features/chatbot/chatbot_routes.py
import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.features.chatbot.chatbot_models import ChatPayload
from app.features.chatbot.chatbot_service import ChatbotService
from app.features.chatbot.chatbot_repository import ChatbotRepository

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/session", response_model=ChatPayload, status_code=status.HTTP_201_CREATED)
def initialize_chat_session(db: Session = Depends(get_db)):
    """
    Generates a unique session ID on the backend and seeds a welcome message.
    The frontend should call this when the chat window opens and save this session_id.
    """
    # 1. Generate a completely unique backend session token
    new_session_id = str(uuid.uuid4())
    
    # 2. Seed an initial greeting message into SQLite history so the model has opening context
    welcome_text = "Hello! I am your TenX E-Commerce Assistant. How can I help you with our products or policies today?"
    ChatbotRepository.create_message(
        db=db,
        session_id=new_session_id,
        role="model",
        content=welcome_text,
    )

    return ChatPayload(session_id=new_session_id, message=welcome_text)

@router.post("/message")
def post_chat_message(payload: ChatPayload, db: Session = Depends(get_db)):
    # This stays exactly the same, receiving the backend-generated session_id from the client
    ai_response = ChatbotService.process_chat(
        db=db, 
        session_id=payload.session_id, 
        user_message=payload.message
    )
    return {"response": ai_response}