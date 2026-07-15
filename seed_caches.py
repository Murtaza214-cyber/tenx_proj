# seed_caches.py
import sys
import os

# Ensure the app directory is in the system path for clean imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.features.chatbot.cache_service import ExactCacheService, SemanticCacheService
from app.config.redis import redis_client

# 📋 Sample E-Commerce Knowledge Base (FAQs)
FAQ_DATA = [
    {
        "query": "What is your return policy?",
        "response": "We offer a hassle-free 30-day return policy! Items must be unused, in their original packaging, and accompanied by the receipt. Returns can be initiated through your profile dashboard."
    },
    {
        "query": "How long does shipping take?",
        "response": "Standard delivery takes 3 to 5 business days within Pakistan. Express shipping options are available at checkout for guaranteed 1-2 day delivery."
    },
    {
        "query": "Do you offer international shipping?",
        "response": "Currently, we only ship orders domestically within Pakistan. We hope to expand to international shipping in the near future!"
    },
    {
        "query": "What payment methods do you accept?",
        "response": "We accept Cash on Delivery (COD), Visa, Mastercard, EasyPaisa, and JazzCash."
    },
    {
        "query": "How can I track my order?",
        "response": "Once your order is dispatched, we will send you an email and SMS containing your tracking number and carrier link. You can also track it directly on our portal by typing your order ID."
    },
    {
        "query": "Can I cancel or change my order?",
        "response": "Orders can be canceled or modified within 1 hour of placement. After 1 hour, the order enters processing and cannot be changed. Please contact our support line immediately for urgent changes."
    }
]

def seed_database_caches():
    print("🚀 Starting Cache Seeding Process...")
    
    # 1. Check Redis Connection
    try:
        redis_client.ping()
        print("🟢 Connected to Redis successfully.")
    except Exception as e:
        print(f"❌ Could not connect to Redis: {e}")
        print("💡 Make sure your Docker Redis container or local Redis server is running!")
        sys.exit(1)

    # 2. Initialize Cache Services
    print("🧠 Loading local SentenceTransformer model (this might take a second)...")
    exact_cache = ExactCacheService()
    semantic_cache = SemanticCacheService()

    # 3. Clear existing cache entries to avoid duplicate clutter (Optional)
    print("🧹 Flushing old cache keys...")
    existing_exact = redis_client.keys("exact_cache:*")
    existing_semantic = redis_client.keys("semantic_cache:*")
    for key in existing_exact + existing_semantic:
        redis_client.delete(key)

    # 4. Populate Caches
    print(f"📥 Seeding {len(FAQ_DATA)} FAQs into Cache layers...")
    for entry in FAQ_DATA:
        q = entry["query"]
        r = entry["response"]
        
        # Seed Exact Cache
        exact_cache.set(q, r)
        
        # Seed Semantic Cache (This generates and saves the local vector embeddings)
        semantic_cache.set(q, r)
        
        print(f"  ✅ Cached: '{q}'")

    print("\n🎉 Caches seeded successfully! Both Exact and Semantic caches are warm and ready.")

if __name__ == "__main__":
    seed_database_caches()