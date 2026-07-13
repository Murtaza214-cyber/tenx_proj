# app/features/chatbot/chatbot_service.py
import os
from google import genai
from google.genai import types
from sqlalchemy.orm import Session
from app.features.chatbot.chatbot_repository import ChatbotRepository
from app.features.chatbot.chatbot_tools import (
    GEMINI_TOOL_LIST,
    query_order_status_db,
    query_product_details_db
)
from app.features.chatbot.chatbot_config import SYSTEM_INSTRUCTION

class ChatbotService:
    @staticmethod
    def process_chat(db: Session, session_id: str, user_message: str):
        api_key = ""
        
        client = genai.Client(api_key=api_key)

        # 1. Log incoming user statement
        ChatbotRepository.create_message(db, session_id=session_id, role="user", content=user_message)

        # 2. Map tool names to actual database executing functions
        tool_execution_map = {
            "verify_order_status": lambda args: query_order_status_db(db, **args),
            "search_product_details": lambda args: query_product_details_db(db, **args)
        }

        # 3. Configure SDK (Gemini only sees the wrappers with simple parameter signatures)
        config = types.GenerateContentConfig(
            tools=GEMINI_TOOL_LIST,
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.2,
        )

        # 4. Call the Gemini model
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=user_message,
            config=config
        )

        # 5. Handle Function Execution Calls safely
        if response.function_calls:
            for call in response.function_calls:
                execution_target = tool_execution_map.get(call.name)
                if execution_target:
                    # Execute the DB query with our intercepted args and active db session
                    tool_result = execution_target(call.args)
                    
                    final_response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=[
                            types.Content(role="user", parts=[types.Part.from_text(text=user_message)]),
                            response.candidates[0].content,
                            types.Content(role="tool", parts=[types.Part.from_function_response(
                                name=call.name,
                                response=tool_result
                            )])
                        ],
                        config=config
                    )
                    ai_response = final_response.text
        else:
            ai_response = response.text

        # 6. Save model output to SQLite
        ChatbotRepository.create_message(db, session_id=session_id, role="model", content=ai_response)
        return ai_response