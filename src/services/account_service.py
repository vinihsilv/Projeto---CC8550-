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
        self.repository.create(
            Account(
                id=next_id, name=name, user_id=user_id, balance=0.0  # saldo inicial
            )
        )

    def list_accounts(self, user_id: int) -> List[Account]:
        return [a for a in self.repository.list() if a.user_id == user_id]

    def get_account(self, account_id: int) -> Account:
        account = self.repository.get(account_id)
        if not account:
            raise ValueError("Account not found")
        return account

    def update_account(
        self, account_id: int, name: str | None = None, balance: float | None = None
    ):
        data = {}
        if name is not None:
            data["name"] = name
        if balance is not None:
            data["balance"] = balance

        if not data:
            raise ValueError("Nenhum dado para atualizar.")

        self.repository.update(account_id, data)

    def delete_account(self, account_id: int, user_id: int):
        account = self.repository.get(account_id)
        if not account or account.user_id != user_id:
            raise ValueError("Conta não encontrada ou pertence a outro usuário")
        self.repository.delete(account_id)
