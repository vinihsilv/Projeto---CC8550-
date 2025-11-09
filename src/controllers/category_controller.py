# src/controllers/category_controller.py
from src.services.category_service import CategoryService
from src.repositories.category_repository import CategoryRepository


class CategoryController:
    def __init__(self):
        repo = CategoryRepository()
        self.service = CategoryService(repo)

    def create_category(self, name, user_id):
        return self.service.create_category(name, user_id)

    def list_categories(self, user_id):
        return self.service.list_categories(user_id)

    def get_category(self, category_id):
        return self.service.get_category(category_id)

    def update_category(self, category_id, data):
        self.service.update_category(category_id, data)

    def delete_category(self, category_id):
        self.service.delete_category(category_id)
