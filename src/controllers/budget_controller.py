# src/controllers/budget_controller.py
from src.repositories.account_repository import AccountRepository
from src.services.budget_service import BudgetService
from src.repositories.budget_repository import BudgetRepository
from src.repositories.category_repository import CategoryRepository


class BudgetController:
    def __init__(
        self,
        repo: BudgetRepository,
        account_repo: AccountRepository,
        category_repo: CategoryRepository,
    ):
        self.service = BudgetService(repo)

    def create_budget(self, user_id, category_id, year, month, limit_value):
        self.service.create_budget(user_id, category_id, year, month, limit_value)

    def list_budgets(self, user_id: int):
        return self.service.list_budgets(user_id)

    def get_budget(self, budget_id):
        return self.service.get_budget(budget_id)

    def update_budget(self, budget_id, data):
        self.service.update_budget(budget_id, data)

    def delete_budget(self, budget_id):
        self.service.delete_budget(budget_id)
