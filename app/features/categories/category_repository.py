# app/features/categories/category_repository.py
from sqlalchemy.orm import Session
from app.features.categories.category_models import CategoryDB, CategoryCreate

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str):
        return self.db.query(CategoryDB).filter(CategoryDB.name == name).first()

    def get_by_id(self, category_id: int):
        return self.db.query(CategoryDB).filter(CategoryDB.id == category_id).first()

    def create(self, category_data: CategoryCreate):
        category = CategoryDB(name=category_data.name)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def get_all(self):
        return self.db.query(CategoryDB).all()