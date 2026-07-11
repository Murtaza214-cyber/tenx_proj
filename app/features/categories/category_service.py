from app.features.categories.category_repository import CategoryRepository
from app.features.categories.category_models import CategoryCreate

class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def get_or_create_category(self, name: str):
        category = self.repository.get_by_name(name)
        if not category:
            new_cat = CategoryCreate(name=name)
            category = self.repository.create(new_cat)
        return category

    def list_categories(self):
        return self.repository.get_all()