import os
from google import genai
from sqlalchemy.orm import Session
from app.features.chatbot.chatbot_repository import ChatbotRepository

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class ChatbotService:
    @staticmethod
    def process_chat(db: Session, user_message: str):
        # 1. Save the incoming user message using the repository layer
        ChatbotRepository.create_message(db, role="user", content=user_message)
        
        # 2. Call the Gemini API
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        ai_response = response.text
        
        # 3. Save the generated response from Gemini using the repository layer
        saved_ai_message = ChatbotRepository.create_message(db, role="model", content=ai_response)
        
        return saved_ai_message