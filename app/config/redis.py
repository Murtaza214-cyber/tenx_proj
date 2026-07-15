# app/config/redis.py
import redis

from app.config.settings import REDIS_URL

# Connect to your local Redis instance (default port is 6379)
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def get_redis():
    """Dependency provider for FastAPI endpoints if needed."""
    return redis_client