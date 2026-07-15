# app/features/chatbot/chatbot_service.py
import time
from datetime import datetime
from google import genai
from google.genai import types
from sqlalchemy.orm import Session

from app.features.chatbot.chatbot_repository import ChatbotRepository
from app.features.chatbot.chatbot_tools import (
    GEMINI_TOOL_LIST,
    query_order_status_db,
    query_product_details_db
)
from app.config.settings import GEMINI_API_KEY
from app.features.chatbot.chatbot_config import SYSTEM_INSTRUCTION
from app.features.chatbot.cache_service import ExactCacheService, SemanticCacheService
from app.utils.logger_utils import diagnostics_logger

semantic_cache = SemanticCacheService()
exact_cache = ExactCacheService()

class ChatbotService:
    @staticmethod
    def process_chat(db: Session, session_id: str, user_message: str, cache_mode: str = "semantic"):
        """Process a chatbot request with caching, LLM generation, and diagnostics logging."""
        start_time = time.perf_counter()
        cached_response = None
        cache_status = "MISS"
        cache_hits = 0
        db_hits = 0

        ChatbotRepository.create_message(db, session_id=session_id, role="user", content=user_message)
        db_hits += 1

        if cache_mode == "exact":
            cached_response = exact_cache.get(user_message)
            if cached_response:
                cache_status = "HIT"
                cache_hits = 1
        elif cache_mode == "semantic":
            cached_response = semantic_cache.get(user_message)
            if cached_response:
                cache_status = "HIT"
                cache_hits = 1
        else:
            cache_status = "DISABLED"

        if cached_response:
            latency_ms = (time.perf_counter() - start_time) * 1000

            ChatbotRepository.create_message(db, session_id=session_id, role="model", content=cached_response)
            db_hits += 1

            diagnostics_logger.info(
                f"{datetime.now().isoformat()},{session_id},{cache_mode},{cache_status},{cache_hits},{db_hits},{latency_ms:.2f},\"{user_message}\""
            )
            
            return cached_response

        # Fall back to Gemini when no cache result is available
        client = genai.Client(api_key=GEMINI_API_KEY)

        db_history = ChatbotRepository.get_session_history(db, session_id=session_id)
        db_hits += 1

        contents_payload = []
        for msg in db_history:
            if isinstance(msg, dict):
                role = msg.get("role")
                content = msg.get("content")
            else:
                role = getattr(msg, "role", None)
                content = getattr(msg, "content", None)

            if role is None or content is None:
                continue
            contents_payload.append(
                types.Content(role=role, parts=[types.Part.from_text(text=content)])
            )
        contents_payload.append(
            types.Content(role="user", parts=[types.Part.from_text(text=user_message)])
        )

        tool_execution_map = {
            "verify_order_status": lambda args: query_order_status_db(db, **args),
            "search_product_details": lambda args: query_product_details_db(db, **args)
        }

        config = types.GenerateContentConfig(
            tools=GEMINI_TOOL_LIST,
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.2,
        )

        response = client.models.generate_content(
            model='gemini-3.0-flash',
            contents=contents_payload,
            config=config
        )

        if response.function_calls:
            for call in response.function_calls:
                execution_target = tool_execution_map.get(call.name)
                if execution_target:
                    tool_result = execution_target(call.args)
                    db_hits += 1
                    contents_payload.append(response.candidates[0].content)
                    contents_payload.append(
                        types.Content(role="tool", parts=[types.Part.from_function_response(
                            name=call.name, response=tool_result
                        )])
                    )
                    final_response = client.models.generate_content(
                        model='gemini-3.0-flash',
                        contents=contents_payload,
                        config=config
                    )
                    ai_response = final_response.text
        else:
            ai_response = response.text

        if cache_mode == "exact":
            exact_cache.set(user_message, ai_response)
        elif cache_mode == "semantic":
            exact_cache.set(user_message, ai_response)
            semantic_cache.set(user_message, ai_response)

        ChatbotRepository.create_message(db, session_id=session_id, role="model", content=ai_response)
        db_hits += 1

        latency_ms = (time.perf_counter() - start_time) * 1000
        diagnostics_logger.info(
            f"{datetime.now().isoformat()},{session_id},{cache_mode},{cache_status},{cache_hits},{db_hits},{latency_ms:.2f},\"{user_message}\""
        )

        return ai_response