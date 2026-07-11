# app/features/products/product_repository.py
from sqlalchemy.orm import Session
from app.features.products.product_models import ProductDB, ProductCreate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_product(self, product_id: int):
        return self.db.query(ProductDB).filter(ProductDB.id == product_id).first()

    def create_product(self, product_data: ProductCreate, category_id: int):
        product = ProductDB(
            title=product_data.title,
            price=product_data.price,
            stock=product_data.stock,
            category_id=category_id
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_stock(self, product_id: int, new_stock: int):
        product = self.get_product(product_id)
        if product:
            product.stock = new_stock
            self.db.commit()

    def get_all_products(self):
        return self.db.query(ProductDB).all()

    def product_exists_by_title(self, title: str):
        return self.db.query(ProductDB).filter(ProductDB.title == title).first() is not None