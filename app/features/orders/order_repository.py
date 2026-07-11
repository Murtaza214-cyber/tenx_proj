# app/features/orders/order_repository.py
from sqlalchemy.orm import Session
from .order_models import OrderDB

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, user_id: int, product_id: int, quantity: int, total_price: float):
        order = OrderDB(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price,
            status="Completed"
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order