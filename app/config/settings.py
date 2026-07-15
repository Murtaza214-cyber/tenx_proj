import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-change-me-in-production")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "another-super-secret-for-refresh-tokens")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
