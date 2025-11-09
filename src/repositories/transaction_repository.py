from src.interfaces.transaction_repository_interface import ITransactionRepository
from src.models.transaction import Transaction


class TransactionRepository(ITransactionRepository):

    def __init__(self):
        self.transactions: list[Transaction] = []
        self.next_id = 1

    def create(self, transaction: Transaction):
        transaction.id = self.next_id
        self.next_id += 1
        self.transactions.append(transaction)
        return transaction

    def list_all(self):
        return self.transactions

    def get_by_id(self, transaction_id: int):
        return next((t for t in self.transactions if t.id == transaction_id), None)

    def list_by_user(self, user_id: int):
        return [t for t in self.transactions if t.user_id == user_id]

    def list_by_category(self, category_id: int):
        return [t for t in self.transactions if t.category_id == category_id]

    def update(self, transaction_id: int, data: dict):
        transaction = self.get_by_id(transaction_id)
        if not transaction:
            return None

        transaction.amount = data.get("amount", transaction.amount)
        transaction.type = data.get("type", transaction.type)
        transaction.date = data.get("date", transaction.date)
        transaction.category_id = data.get("category_id", transaction.category_id)
        transaction.description = data.get("description", transaction.description)
        transaction.user_id = data.get("user_id", transaction.user_id)

        return transaction

    def delete(self, transaction_id: int):
        transaction = self.get_by_id(transaction_id)
        if transaction:
            self.transactions.remove(transaction)
            return True
        return False
