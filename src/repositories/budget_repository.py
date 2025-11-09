from typing import List
from src.models.budget import Budget
from src.interfaces.budget_repository_interface import BudgetRepositoryInterface


class BudgetRepository:
    def __init__(self):
        self._budgets = []

    def create(self, budget):
        self._budgets.append(budget)

    def list(self):
        return self._budgets

    def get(self, budget_id):
        for b in self._budgets:
            if b.id == budget_id:
                return b
        return None

    def update(self, budget):
        pass

    def delete(self, budget_id):
        self._budgets = [b for b in self._budgets if b.id != budget_id]
