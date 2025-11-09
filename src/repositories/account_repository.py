# src/repositories/account_repository.py
from typing import List
from src.models.account import Account
from src.interfaces.account_repository_interface import AccountRepositoryInterface


class AccountRepository(AccountRepositoryInterface):
    def __init__(self):
        self._accounts: List[Account] = []

    def create(self, account: Account) -> None:
        self._accounts.append(account)

    def list(self, user_id: int) -> List[Account]:
        return [a for a in self._accounts if a.user_id == user_id]

    def get(self, account_id: int) -> Account | None:
        for a in self._accounts:
            if a.id == account_id:
                return a
        return None

    def update(self, account_id: int, data: dict) -> None:
        account = self.get(account_id)
        if account:
            account.name = data.get("name", account.name)
            if "balance" in data:
                account.balance = data["balance"]

    def delete(self, account_id: int) -> None:
        self._accounts = [a for a in self._accounts if a.id != account_id]
