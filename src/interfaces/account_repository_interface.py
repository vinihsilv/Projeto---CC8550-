# src/interfaces/account_repository_interface.py
from abc import ABC, abstractmethod
from typing import List
from src.models.account import Account


class AccountRepositoryInterface(ABC):
    @abstractmethod
    def create(self, account: Account) -> None:
        pass

    @abstractmethod
    def list(self) -> List[Account]:
        pass

    @abstractmethod
    def update(self, account_id: int, data: dict) -> None:
        pass

    @abstractmethod
    def delete(self, account_id: int) -> None:
        pass

    @abstractmethod
    def get(self, account_id: int) -> Account | None:
        pass
