from abc import ABC, abstractmethod
from src.models.category import Category


class ICategoryRepository(ABC):

    @abstractmethod
    def create(self, category: Category):
        pass

    @abstractmethod
    def list_all(self):
        pass

    @abstractmethod
    def get_by_id(self, category_id: int):
        pass

    @abstractmethod
    def update(self, category_id: int, name: str, description: str | None):
        pass

    @abstractmethod
    def delete(self, category_id: int):
        pass
