# app/features/products/product_service.py
from fastapi import HTTPException
from app.features.products.product_repository import ProductRepository
from app.features.products.product_models import ProductCreate
from app.features.categories.category_service import CategoryService # Import across boundaries

class ProductService:
    # Inject both its own repository and the external category service
    def __init__(self, repository: ProductRepository, category_service: CategoryService):
        self.repository = repository
        self.category_service = category_service

    def catalog_new_product(self, product_data: ProductCreate):
        if self.repository.product_exists_by_title(product_data.title):
            raise HTTPException(
                status_code=400,
                detail=f"Product with title '{product_data.title}' already exists"
            )
        
        category = self.category_service.get_or_create_category(product_data.category_name)
        
        return self.repository.create_product(product_data, category.id)

    def verify_and_deduct_stock(self, product_id: int, quantity: int) -> bool:
        product = self.repository.get_product(product_id)
        if not product or product.stock < quantity:
            return False
        
        new_stock = product.stock - quantity
        self.repository.update_stock(product_id, new_stock)
        return True
    
    