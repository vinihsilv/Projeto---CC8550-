from src.models.category import Category
from src.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self):
        self.repository = CategoryRepository()

    def create_category(self, name: str, description: str | None = None):
        category = Category(id=None, name=name, description=description)
        return self.repository.create(category)

    def list_categories(self):
        return self.repository.list_all()

    def update_category(self, category_id: int, name: str, description: str | None):
        return self.repository.update(category_id, name, description)

    def delete_category(self, category_id: int):
        return self.repository.delete(category_id)

    def get_category(self, category_id: int):
        return self.repository.get_by_id(category_id)
