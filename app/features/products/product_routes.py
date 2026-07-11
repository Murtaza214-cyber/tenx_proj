# app/features/products/product_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.features.products.product_models import ProductCreate, ProductResponse
from app.features.products.product_repository import ProductRepository
from app.features.products.product_service import ProductService
from app.features.categories.category_repository import CategoryRepository
from app.features.categories.category_service import CategoryService

router = APIRouter(prefix="/products", tags=["Products"])

def get_product_service(db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    category_repo = CategoryRepository(db)
    category_service = CategoryService(category_repo)
    
    return ProductService(repository=product_repo, category_service=category_service)

@router.post("/", response_model=ProductResponse)
def create_product(payload: ProductCreate, service: ProductService = Depends(get_product_service)):
    return service.catalog_new_product(payload)

@router.get("/", response_model=list[ProductResponse])
def get_all_products(service: ProductService = Depends(get_product_service)):
    return service.repository.get_all_products()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int, service: ProductService = Depends(get_product_service)):
    return service.repository.get_product(product_id)