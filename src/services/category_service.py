# src/services/category_service.py
from typing import List
from src.models.category import Category
from src.repositories.category_repository import CategoryRepositoryInterface
from src.services.exceptions import (
    CategoryNotFoundError,
    NoDataToUpdateError,
    CategoryInUseError,
)


class CategoryService:
    def __init__(self, repository: CategoryRepositoryInterface):
        self.repository = repository

    def create_category(self, name: str, user_id: int):
        if not name or not name.strip():
            raise NoDataToUpdateError("Nome da categoria é obrigatório.")
        category = Category(name=name.strip(), user_id=user_id)
        self.repository.create(category)
        return category

    def list_categories(self, user_id: int) -> List[Category]:
        return [c for c in self.repository.list_all() if c.user_id == user_id]

    def get_category(self, category_id: int) -> Category:
        category = self.repository.get_category(category_id)
        if not category:
            raise CategoryNotFoundError("Category not found")
        return category

    def update_category(self, category_id: int, data: dict) -> None:
        category = self.get_category(category_id)
        if "name" in data:
            self.repository.update(category_id, data["name"])

    def delete_category(self, category_id: int) -> None:
        category = self.get_category(category_id)
        self.repository.delete(category_id)
