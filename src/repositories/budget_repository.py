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

    def update(self, budget_id: int, data: dict) -> None:
        budget = self.get(budget_id)
        if not budget:
            raise ValueError("Budget not found")

        # Atualiza apenas os campos que existem em data
        for key, value in data.items():
            if hasattr(budget, key):
                setattr(budget, key, value)

    def delete(self, budget_id):
        self._budgets = [b for b in self._budgets if b.id != budget_id]

    def list_by_category(self, category_id: int, user_id: int):
        # Retorna orçamento do usuário para aquela categoria, se existir
        return next(
            (
                b
                for b in self._budgets
                if b.category_id == category_id and b.user_id == user_id
            ),
            None,
        )
