# src/services/account_service.py
from typing import List
from src.models.account import Account
from src.repositories.account_repository import AccountRepositoryInterface


class AccountService:
    def __init__(self, repository: AccountRepositoryInterface):
        self.repository = repository

    def create_account(self, name: str, user_id: int) -> None:
        next_id = (
            1
            if not self.repository.list()
            else max(a.id for a in self.repository.list()) + 1
        )
        self.repository.create(Account(id=next_id, name=name, user_id=user_id))

    def list_accounts(self, user_id: int) -> List[Account]:
        return [a for a in self.repository.list() if a.user_id == user_id]

    def get_account(self, account_id: int) -> Account:
        account = self.repository.get(account_id)
        if not account:
            raise ValueError("Account not found")
        return account

    def update_account(self, account_id: int, data: dict) -> None:
        account = self.get_account(account_id)
        self.repository.update(account_id, data)

    def delete_account(self, account_id: int) -> None:
        account = self.get_account(account_id)
        self.repository.delete(account_id)
