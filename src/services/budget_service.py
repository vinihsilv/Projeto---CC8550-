from src.models.budget import Budget
from src.repositories.budget_repository import BudgetRepository


class BudgetService:
    def __init__(self):
        self.repository = BudgetRepository()

    def create_budget(self, category_id, year, month, limit_value):
        budgets = self.repository.list()

        next_id = 1 if not budgets else max(b.id for b in budgets) + 1

        budget = Budget(
            id=next_id,
            category_id=int(category_id),
            year=int(year),
            month=int(month),
            limit_value=float(limit_value),
        )

        self.repository.create(budget)

    def list_budgets(self):
        return self.repository.list()

    def update_budget(
        self, budget_id, category_id=None, year=None, month=None, limit_value=None
    ):
        budget = self.repository.get(int(budget_id))
        if not budget:
            raise ValueError("Orçamento não encontrado.")

        if category_id is not None:
            budget.category_id = int(category_id)

        if year is not None:
            budget.year = int(year)

        if month is not None:
            budget.month = int(month)

        if limit_value is not None:
            budget.limit_value = float(limit_value)

        self.repository.update(budget)

    def delete_budget(self, budget_id):
        self.repository.delete(int(budget_id))
