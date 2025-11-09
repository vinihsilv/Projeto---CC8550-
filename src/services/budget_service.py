# src/services/budget_service.py
from typing import List
from src.models.budget import Budget
from src.repositories.budget_repository import BudgetRepositoryInterface


class BudgetService:
    def __init__(self, repository: BudgetRepositoryInterface):
        self.repository = repository

    def create_budget(
        self, user_id: int, category_id: int, year: int, month: int, limit_value: float
    ):
        next_id = (
            1
            if not self.repository.list()
            else max(b.id for b in self.repository.list()) + 1
        )
        self.repository.create(
            Budget(
                id=next_id,
                user_id=user_id,
                month=month,
                category_id=category_id,
                year=year,
                limit_value=limit_value,
            )
        )

    def list_budgets(self, user_id: int):
        # filtra somente budgets do usuário
        return [b for b in self.repository.list() if b.user_id == user_id]

    def get_budget(self, budget_id: int) -> Budget:
        budget = self.repository.get(budget_id)
        if not budget:
            raise ValueError("Budget not found")
        return budget

    def update_budget(self, budget_id: int, data: dict) -> None:
        budget = self.get_budget(budget_id)
        self.repository.update(budget_id, data)

    def delete_budget(self, budget_id: int) -> None:
        budget = self.get_budget(budget_id)
        self.repository.delete(budget_id)
