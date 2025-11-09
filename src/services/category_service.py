# src/services/category_service.py
from typing import List
from src.models.category import Category
from src.repositories.category_repository import CategoryRepositoryInterface


class CategoryService:
    def __init__(self, repository: CategoryRepositoryInterface):
        self.repository = repository

    def create_category(self, name: str, user_id: int) -> None:
        next_id = (
            1
            if not self.repository.list_all()
            else max(c.id for c in self.repository.list_all()) + 1
        )
        self.repository.create(Category(id=next_id, name=name, user_id=user_id))

    def list_categories(self, user_id: int) -> List[Category]:
        all_cats = self.repository.list_all()
        filtered = [c for c in all_cats if c.user_id == user_id]
        return filtered

    def get_category(self, category_id: int) -> Category:
        category = self.repository.get_category(category_id)
        if not category:
            raise ValueError("Category not found")
        return category

    def update_category(self, category_id: int, data: dict) -> None:
        category = self.get_category(category_id)
        self.repository.update(category_id, data)

    def delete_category(self, category_id: int) -> None:
        category = self.get_category(category_id)
        self.repository.delete(category_id)
