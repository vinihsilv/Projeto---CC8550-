from abc import ABC, abstractmethod
from typing import List
from src.models.budget import Budget


class BudgetRepositoryInterface(ABC):

    @abstractmethod
    def create(self, budget: Budget) -> None:
        pass

    @abstractmethod
    def list(self) -> List[Budget]:
        pass

    @abstractmethod
    def update(self, budget_id: int, data: dict) -> None:
        pass

    @abstractmethod
    def delete(self, budget_id: int) -> None:
        pass
