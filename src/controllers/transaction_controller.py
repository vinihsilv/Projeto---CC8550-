from src.services.transaction_service import TransactionService
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.account_repository import AccountRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.budget_repository import BudgetRepository
from src.utils.database import SessionLocal  # nossa factory de sessão SQLAlchemy


class TransactionController:
    def __init__(self, transaction_repo, account_repo, category_repo, budget_repo):
        self.service = TransactionService(
            transaction_repo, account_repo, category_repo, budget_repo
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

    def search_transactions_with_filters(
        self,
        user_id,
        transaction_type=None,
        min_amount=None,
        max_amount=None,
        start_date=None,
        end_date=None,
        category_id=None,
        account_id=None,
        description_contains=None,
        sort_by="date",
        sort_order="desc",
    ):
        """Busca transações com filtros avançados."""
        return self.service.search_transactions_with_filters(
            user_id=user_id,
            transaction_type=transaction_type,
            min_amount=min_amount,
            max_amount=max_amount,
            start_date=start_date,
            end_date=end_date,
            category_id=category_id,
            account_id=account_id,
            description_contains=description_contains,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    def get_transactions_summary(
        self,
        user_id,
        group_by="category",
        period_start=None,
        period_end=None,
        transaction_type=None,
        sort_by="total_amount",
        sort_order="desc",
    ):
        """Obtém resumo de transações agrupadas."""
        return self.service.get_transactions_summary(
            user_id=user_id,
            group_by=group_by,
            period_start=period_start,
            period_end=period_end,
            transaction_type=transaction_type,
            sort_by=sort_by,
            sort_order=sort_order,
        )
