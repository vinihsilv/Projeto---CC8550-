# src/services/account_service.py
from src.models.account import Account
from src.repositories.account_repository import AccountRepository


class AccountService:
    def __init__(self):
        self.repository = AccountRepository()

    def create_account(self, user_id: int, name: str, balance: float) -> None:
        accounts = self.repository.list(user_id)
        next_id = 1 if not accounts else max(a.id for a in accounts) + 1
        account = Account(id=next_id, name=name, balance=balance, user_id=user_id)
        self.repository.create(account)

    def list_accounts(self, user_id: int):
        return self.repository.list(user_id)

    def update_account(
        self, account_id: int, name: str | None = None, balance: float | None = None
    ):
        data = {}
        if name:
            data["name"] = name
        if balance is not None:
            data["balance"] = balance
        self.repository.update(account_id, data)

    def delete_account(self, account_id: int):
        self.repository.delete(account_id)
