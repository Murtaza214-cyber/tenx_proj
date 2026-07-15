# app/features/chatbot/chatbot_routes.py
import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.features.chatbot.chatbot_models import ChatPayload
from app.features.chatbot.chatbot_service import ChatbotService
from app.features.chatbot.chatbot_repository import ChatbotRepository
from app.utils.regex_utils import RegexUtils
from app.features.chatbot.chatbot_tools import query_order_status_db

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post("/session", response_model=ChatPayload, status_code=status.HTTP_201_CREATED)
def initialize_chat_session(db: Session = Depends(get_db)):
    """
    Generates a unique session ID on the backend and seeds a welcome message.
    """
    new_session_id = str(uuid.uuid4())
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
    """
    Receives user messages, supporting configurable caching layers.
    """
    user_msg = payload.message

    # Skip cache logic entirely if user uses regex to fetch order details directly
    extracted_order_id = RegexUtils.extract_order_id(user_msg)
    if extracted_order_id is not None:
        ChatbotRepository.create_message(db, session_id=payload.session_id, role="user", content=user_msg)
        order_data = query_order_status_db(db, order_id=extracted_order_id)
        if "error" not in order_data:
            ai_response = (
                f"I found your order! **Order ORD-{order_data['order_id']}** is currently **{order_data['status']}**. "
                f"It contains {order_data['quantity']} item(s) with a total of Rs. {order_data['total_price']:.2f}."
            )
            ChatbotRepository.create_message(db, session_id=payload.session_id, role="model", content=ai_response)
            return {"response": ai_response}

    # Pass the client-specified cache_mode configuration
    ai_response = ChatbotService.process_chat(
        db=db, 
        session_id=payload.session_id, 
        user_message=user_msg,
        cache_mode=payload.cache_mode
    )
    return {"response": ai_response}