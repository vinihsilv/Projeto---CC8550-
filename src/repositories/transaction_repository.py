from sqlalchemy.orm import Session
from src.interfaces.transaction_repository_interface import (
    TransactionRepositoryInterface,
)
from src.models.transaction import Transaction


class TransactionRepository(TransactionRepositoryInterface):
    """SQLAlchemy implementation of TransactionRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def list_all(self) -> list[Transaction]:
        return self.session.query(Transaction).all()

    def get_by_id(self, transaction_id: int) -> Transaction | None:
        return self.session.query(Transaction).filter_by(id=transaction_id).first()

    def list_by_user(self, user_id: int) -> list[Transaction]:
        return self.session.query(Transaction).filter_by(user_id=user_id).all()

    def list_by_account(self, account_id: int) -> list[Transaction]:
        return self.session.query(Transaction).filter_by(account_id=account_id).all()

    def list_by_category(self, category_id: int, user_id: int) -> list[Transaction]:
        return (
            self.session.query(Transaction)
            .filter_by(category_id=category_id, user_id=user_id)
            .all()
        )

    def update(self, transaction_id: int, data: dict) -> Transaction | None:
        transaction = self.get_by_id(transaction_id)
        if not transaction:
            return None

        for key in [
            "amount",
            "type",
            "date",
            "account_id",
            "category_id",
            "description",
            "user_id",
        ]:
            if key in data:
                setattr(transaction, key, data[key])

        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def delete(self, transaction_id: int) -> bool:
        transaction = self.get_by_id(transaction_id)
        if transaction:
            self.session.delete(transaction)
            self.session.commit()
            return True
        return False
