from abc import ABC, abstractmethod
from src.models.transaction import Transaction


class TransactionRepositoryInterface(ABC):

    @abstractmethod
    def create(self, transaction: Transaction):
        pass

    @abstractmethod
    def list_all(self):
        pass

    @abstractmethod
    def get_by_id(self, transaction_id: int):
        pass

    @abstractmethod
    def list_by_user(self, user_id: int):
        pass

    @abstractmethod
    def list_by_category(self, category_id: int):
        pass

    @abstractmethod
    def update(self, transaction_id: int, data: dict):
        pass

    @abstractmethod
    def delete(self, transaction_id: int):
        pass
