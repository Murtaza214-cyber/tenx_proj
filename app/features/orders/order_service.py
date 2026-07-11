# app/features/orders/order_service.py
from .order_repository import OrderRepository
from .order_models import OrderCreate
from app.features.users.user_repository import UserRepository
from app.features.products.product_repository import ProductRepository
from app.features.products.product_service import ProductService

class OrderService:
    def __init__(self, order_repo: OrderRepository, user_repo: UserRepository, product_repo: ProductRepository, product_service: ProductService):
        self.order_repo = order_repo
        self.user_repo = user_repo
        self.product_repo = product_repo
        self.product_service = product_service

    def place_order(self, order_data: OrderCreate):
        # 1. Validation Rule: Does user exist?
        user = self.user_repo.get_by_id(order_data.user_id)
        if not user:
            raise ValueError("User not found")

        # 2. Validation Rule: Does product exist?
        product = self.product_repo.get_product(order_data.product_id)
        if not product:
            raise ValueError("Product not found")

        # 3. Domain Coordination: Inventory validation and reduction
        stock_deducted = self.product_service.verify_and_deduct_stock(order_data.product_id, order_data.quantity)
        if not stock_deducted:
            raise ValueError("Insufficient inventory stock")

        # 4. Calculation Logic
        total_price = product.price * order_data.quantity

        # 5. Persist
        return self.order_repo.create_order(
            user_id=order_data.user_id,
            product_id=order_data.product_id,
            quantity=order_data.quantity,
            total_price=total_price
        )