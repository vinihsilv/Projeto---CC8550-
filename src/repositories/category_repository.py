from src.interfaces.category_repository_interface import ICategoryRepository
from src.models.category import Category


class CategoryRepository(ICategoryRepository):
    def __init__(self):
        self.categories: list[Category] = []
        self.next_id = 1

    def create(self, category: Category):
        category.id = self.next_id
        self.next_id += 1
        self.categories.append(category)
        return category

    def list_all(self):
        return self.categories

    def get_by_id(self, category_id: int):
        return next((c for c in self.categories if c.id == category_id), None)

    def update(self, category_id: int, name: str, description: str | None):
        category = self.get_by_id(category_id)
        if category:
            category.name = name
            category.description = description
            return category
        return None

    def delete(self, category_id: int):
        category = self.get_by_id(category_id)
        if category:
            self.categories.remove(category)
            return True
        return False
