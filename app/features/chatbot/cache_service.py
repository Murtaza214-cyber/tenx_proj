# app/features/chatbot/cache_services.py
import json
import math
from sentence_transformers import SentenceTransformer
from app.config.redis import redis_client

EXACT_PREFIX = "exact_cache:"
SEMANTIC_PREFIX = "semantic_cache:"
SIMILARITY_THRESHOLD = 0.85

class ExactCacheService:
    """Redis-backed exact text match cache."""

    @staticmethod
    def get(query: str) -> str | None:
        """Looks up an exact string match in Redis."""
        key = f"{EXACT_PREFIX}{query.lower().strip().replace(' ', '_')}"
        return redis_client.get(key)

    @staticmethod
    def set(query: str, response: str):
        """Caches an exact string response permanently."""
        key = f"{EXACT_PREFIX}{query.lower().strip().replace(' ', '_')}"
        redis_client.set(key, response)


class SemanticCacheService:
    """Vector similarity cache using local embeddings and Redis storage."""

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def _get_embedding(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()

    def _cosine_similarity(self, vec_a: list[float], vec_b: list[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def get(self, query: str) -> str | None:
        try:
            query_vector = self._get_embedding(query)
            keys = redis_client.keys(f"{SEMANTIC_PREFIX}*")
            if not keys:
                return None

            best_match_response = None
            highest_similarity = -1.0

            for key in keys:
                cached_data_raw = redis_client.get(key)
                if not cached_data_raw:
                    continue
                
                cached_entry = json.loads(cached_data_raw)
                cached_vector = cached_entry.get("embedding")
                similarity = self._cosine_similarity(query_vector, cached_vector)
                
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_match_response = cached_entry.get("response")

            if highest_similarity >= SIMILARITY_THRESHOLD:
                print(f"🎯 Semantic Cache HIT! (Similarity: {highest_similarity:.4f})")
                return best_match_response
        except Exception as e:
            print(f"⚠️ Semantic Cache read error: {e}")
        return None

    def set(self, query: str, response: str):
        try:
            query_vector = self._get_embedding(query)
            cache_key = f"{SEMANTIC_PREFIX}{query.lower().strip().replace(' ', '_')}"
            payload = {
                "query": query,
                "response": response,
                "embedding": query_vector
            }
            redis_client.set(cache_key, json.dumps(payload))
        except Exception as e:
            print(f"⚠️ Semantic Cache write error: {e}")