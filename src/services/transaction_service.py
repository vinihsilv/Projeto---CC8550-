from datetime import datetime
from src.models.transaction import Transaction
from src.repositories.transaction_repository import TransactionRepository


class TransactionService:

    def __init__(self):
        self.repository = TransactionRepository()

    def create_transaction(
        self,
        amount: float,
        type: str,
        date: datetime,
        category_id: int | None,
        description: str | None,
        user_id: int,
    ):

        if type not in ("income", "expense"):
            raise ValueError("Type must be 'income' or 'expense'")

        transaction = Transaction(
            id=None,
            amount=amount,
            type=type,
            date=date,
            category_id=category_id,
            description=description,
            user_id=user_id,
        )

        return self.repository.create(transaction)

    def list_all(self):
        return self.repository.list_all()

    def list_by_user(self, user_id: int):
        return self.repository.list_by_user(user_id)

    def list_by_category(self, category_id: int):
        return self.repository.list_by_category(category_id)

    def update_transaction(self, transaction_id: int, data: dict):
        return self.repository.update(transaction_id, data)

    def delete_transaction(self, transaction_id: int):
        return self.repository.delete(transaction_id)
