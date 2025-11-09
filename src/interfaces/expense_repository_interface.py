from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.expense import Expense


class IExpenseRepository(ABC):

    @abstractmethod
    def create(self, expense: Expense) -> None:
        pass

    @abstractmethod
    def list(self) -> List[Expense]:
        pass

    @abstractmethod
    def get(self, expense_id: int) -> Optional[Expense]:
        pass

    @abstractmethod
    def update(self, expense_id: int, data: dict) -> None:
        pass

    @abstractmethod
    def delete(self, expense_id: int) -> None:
        pass
