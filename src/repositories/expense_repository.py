# src/repositories/expense_repository.py

from typing import List, Optional
from src.interfaces.expense_repository_interface import IExpenseRepository
from src.models.expense import Expense


class ExpenseRepository(IExpenseRepository):

    def __init__(self):
        self.expenses: List[Expense] = []

    def create(self, expense: Expense) -> None:
        self.expenses.append(expense)

    def list(self) -> List[Expense]:
        return self.expenses

    def get(self, expense_id: int) -> Optional[Expense]:
        for e in self.expenses:
            if e.id == expense_id:
                return e
        return None

    def update(self, expense_id: int, data: dict) -> None:
        expense = self.get(expense_id)
        if not expense:
            raise ValueError("Expense not found.")

        for key, value in data.items():
            if value is not None:
                setattr(expense, key, value)

    def delete(self, expense_id: int) -> None:
        expense = self.get(expense_id)
        if not expense:
            raise ValueError("Expense not found.")

        self.expenses.remove(expense)
