# src/services/expense_service.py

from typing import Optional
from src.models.expense import Expense
from src.interfaces.expense_repository_interface import IExpenseRepository


class ExpenseService:

    def __init__(self, repository: IExpenseRepository):
        self.repository = repository

    def create_expense(
        self, category_id: int, value: float, date: str, description: Optional[str]
    ):
        expenses = self.repository.list()
        next_id = 1 if not expenses else max(e.id for e in expenses) + 1

        expense = Expense(
            id=next_id,
            category_id=category_id,
            value=value,
            date=date,
            description=description,
        )
        self.repository.create(expense)

    def list_expenses(self):
        return self.repository.list()

    def update_expense(
        self, expense_id: int, category_id=None, value=None, date=None, description=None
    ):
        data = {
            "category_id": category_id,
            "value": value,
            "date": date,
            "description": description,
        }
        self.repository.update(expense_id, data)

    def delete_expense(self, expense_id: int):
        self.repository.delete(expense_id)
