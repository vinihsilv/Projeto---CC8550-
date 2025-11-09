from datetime import datetime
from typing import Optional
from src.services.expense_service import ExpenseService


class ExpenseController:

    def __init__(self, service):
        self.service = service

    def create_expense(self, category_id, value, date, description):
        return self.service.create_expense(category_id, value, date, description)

    def list_expenses(self):
        return self.service.list_expenses()

    def update_expense(self, expense_id, category_id, value, date, description):
        return self.service.update_expense(
            expense_id, category_id, value, date, description
        )

    def delete_expense(self, expense_id):
        return self.service.delete_expense(expense_id)
