# src/services/budget_service.py
from typing import List
from src.models.budget import Budget
from src.repositories.budget_repository import BudgetRepositoryInterface


class BudgetService:
    def __init__(self, repository: BudgetRepositoryInterface):
        self.repository = repository

    def create_budget(
        self, user_id: int, category_id: int, year: int, month: int, limit_value: float
    ) -> Budget:
        if month < 1 or month > 12:
            raise ValueError("Mês inválido (1-12).")

        if limit_value is None or float(limit_value) <= 0:
            raise ValueError("Limite deve ser positivo.")

        existing = self.repository.list_by_user(user_id)
        # verifica duplicidade por ano/mês para o mesmo usuário
        if any(b.year == year and b.month == month for b in existing):
            raise ValueError("Já existe orçamento para este usuário neste mês.")

        budget = Budget(
            id=None,
            user_id=user_id,
            category_id=category_id,
            year=year,
            month=month,
            limit_value=limit_value,
        )
        self.repository.create(budget)
        return budget

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
