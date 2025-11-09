# src/controllers/budget_controller.py
from src.services.budget_service import BudgetService
from src.repositories.budget_repository import BudgetRepository


class BudgetController:
    def __init__(self):
        repo = BudgetRepository()
        self.service = BudgetService(repo)

    def create_budget(self, category_id, year, limit_value):
        self.service.create_budget(category_id, year, limit_value)

    def list_budgets(self):
        return self.service.list_budgets()

    def get_budget(self, budget_id):
        return self.service.get_budget(budget_id)

    def update_budget(self, budget_id, data):
        self.service.update_budget(budget_id, data)

    def delete_budget(self, budget_id):
        self.service.delete_budget(budget_id)
