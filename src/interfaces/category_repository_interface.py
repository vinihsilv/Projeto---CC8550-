from abc import ABC, abstractmethod
from src.models.category import Category


class CategoryRepositoryInterface(ABC):

    @abstractmethod
    def create(self, category: Category):
        pass

    @abstractmethod
    def list_all(self):
        pass

    @abstractmethod
    def get_category(self, category_id: int):
        pass

    @abstractmethod
    def update(self, category_id: int, name: str):
        pass

    @abstractmethod
    def delete(self, category_id: int):
        pass
