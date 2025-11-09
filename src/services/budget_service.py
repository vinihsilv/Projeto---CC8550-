# src/services/budget_service.py
from typing import List
from src.models.budget import Budget
from src.repositories.budget_repository import BudgetRepositoryInterface


class BudgetService:
    def __init__(self, repository: BudgetRepositoryInterface):
        self.repository = repository

    def create_budget(
        self, user_id: int, category_id: int, year: int, month: int, limit_value: float
    ) -> None:
        budget = Budget(
            id=None,  # o banco vai gerar
            user_id=user_id,
            category_id=category_id,
            year=year,
            month=month,
            limit_value=limit_value,
        )
        self.repository.create(budget)

    def list_budgets(self, user_id: int) -> List[Budget]:
        return self.repository.list_by_user(user_id)

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
