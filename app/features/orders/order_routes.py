# app/features/orders/order_routes.py
from fastapi import APIRouter, Depends, HTTPException , status
from sqlalchemy.orm import Session
from app.config.database import get_db
from .order_models import OrderCreate, OrderResponse
from .order_repository import OrderRepository
from .order_service import OrderService
from app.features.users.user_repository import UserRepository
from app.features.products.product_repository import ProductRepository
from app.features.products.product_service import ProductService
from app.features.categories.category_repository import CategoryRepository
from app.features.categories.category_service import CategoryService

router = APIRouter(prefix="/orders", tags=["Orders"])

# Complex Construction injected gracefully via FastAPI's router system
def get_order_service(db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    category_repo = CategoryRepository(db)
    category_service = CategoryService(category_repo)
    return OrderService(
        order_repo=OrderRepository(db),
        user_repo=UserRepository(db),
        product_repo=product_repo,
        product_service=ProductService(product_repo, category_service)
    )

@router.post("/", response_model=OrderResponse)
def checkout(payload: OrderCreate, service: OrderService = Depends(get_order_service)):
    try:
        return service.place_order(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))