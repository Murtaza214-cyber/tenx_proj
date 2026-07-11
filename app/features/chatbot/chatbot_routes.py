from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.features.chatbot.chatbot_schemas import ChatRequest, ChatResponse
from app.features.chatbot.chatbot_services import ChatbotService

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/message", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def post_chat_message(payload: ChatRequest, db: Session = Depends(get_db)):
    # Hand execution down directly to the service layer
    ai_message = ChatbotService.process_chat(db, user_message=payload.message)
    return ai_message