# app/features/chatbot/chatbot_tools.py
from sqlalchemy.orm import Session
from app.features.orders.order_models import OrderDB
from app.features.products.product_models import ProductDB

# =====================================================================
# 💾 1. Actual Database Query Functions (Hidden from Gemini)
# =====================================================================

def query_order_status_db(db: Session, order_id: int) -> dict:
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if order:
        return {
            "order_id": order.id,
            "status": order.status,
            "quantity": order.quantity,
            "total_price": order.total_price
        }
    return {"error": f"Order ORD-{order_id} was not found in our records."}


def query_product_details_db(db: Session, product_title: str) -> dict:
    product = db.query(ProductDB).filter(ProductDB.title.ilike(f"%{product_title}%")).first()
    if product:
        return {
            "product_id": product.id,
            "title": product.title,
            "price": product.price,
            "stock_status": "In Stock" if product.stock > 0 else "Out of Stock",
            "available_quantity": product.stock
        }
    return {"error": f"No product matching '{product_title}' was found in the inventory catalog."}


# =====================================================================
# 🧠 2. Simple Wrapper Functions (Registered with Gemini)
# =====================================================================

def verify_order_status(order_id: int) -> dict:
    """
    Fetches the tracking status, item quantity, and price breakdown of a specific order.
    Use this whenever a user asks about order tracking, delivery schedules, or order status.
    """
    # This wrapper function has a pristine signature! No complex parameters.
    pass


def search_product_details(product_title: str) -> dict:
    """
    Searches the inventory catalog for a product by its title to find pricing, availability, and stock details.
    Use this when a user asks about product costs, item availability, stock counts, or product details.
    """
    # This wrapper function has a pristine signature! No complex parameters.
    pass


# List of clean schemas sent to Gemini
GEMINI_TOOL_LIST = [verify_order_status, search_product_details]