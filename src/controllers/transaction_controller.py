from src.services.transaction_service import TransactionService
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.account_repository import AccountRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.budget_repository import BudgetRepository
from utils.database import SessionLocal  # nossa factory de sessão SQLAlchemy


class TransactionController:
    def __init__(self):
        self.session = SessionLocal()
        self.transaction_repo = TransactionRepository(self.session)
        self.account_repo = AccountRepository(self.session)
        self.category_repo = CategoryRepository(self.session)
        self.budget_repo = BudgetRepository(self.session)

        self.service = TransactionService(
            self.transaction_repo,
            self.account_repo,
            self.category_repo,
            self.budget_repo,
        )

    def create_transaction(
        self, user_id, amount, type_, account_id, category_id, description=None
    ):
        self.service.create_transaction(
            user_id, amount, type_, account_id, category_id, description
        )

    def list_transactions(self, user_id):
        return self.service.list_transactions(user_id)

    def get_transaction(self, transaction_id):
        return self.service.get_transaction(transaction_id)

    def update_transaction(
        self,
        transaction_id,
        user_id,
        amount=None,
        type_=None,
        category_id=None,
        description=None,
    ):
        self.service.update_transaction(
            transaction_id, user_id, amount, type_, category_id, description
        )

    def delete_transaction(self, transaction_id, user_id):
        self.service.delete_transaction(transaction_id, user_id)
