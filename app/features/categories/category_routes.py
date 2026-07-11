# app/features/categories/category_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.features.categories.category_models import CategoryResponse, CategoryCreate
from app.features.categories.category_repository import CategoryRepository
from app.features.categories.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])

def get_category_service(db: Session = Depends(get_db)):
    return CategoryService(CategoryRepository(db))

@router.get("/", response_model=list[CategoryResponse])
def get_all_categories(service: CategoryService = Depends(get_category_service)):
    return service.list_categories()

@router.post("/", response_model=CategoryResponse)
def create_new_category(payload: CategoryCreate, service: CategoryService = Depends(get_category_service)):
    return service.get_or_create_category(payload.name)