# src/repositories/account_repository.py
from typing import List
from src.models.account import Account
from src.interfaces.account_repository_interface import AccountRepositoryInterface


class AccountRepository(AccountRepositoryInterface):
    def __init__(self):
        self._accounts: List[Account] = []

    def create(self, account: Account) -> None:
        self._accounts.append(account)

    def list(self) -> List[Account]:
        return self._accounts

    def get(self, account_id: int) -> Account | None:
        for a in self._accounts:
            if a.id == account_id:
                return a
        return None

    def update(self, account_id: int, data: dict) -> None:
        """
        Atualiza os campos da conta com base no dicionário 'data'.
        """
        account = self.get(account_id)
        if not account:
            raise ValueError(f"Conta com id {account_id} não encontrada")

        for key, value in data.items():
            if hasattr(account, key):
                setattr(account, key, value)
            else:
                raise ValueError(f"Atributo '{key}' não existe na Account")

    def delete(self, account_id: int) -> None:
        self._accounts = [a for a in self._accounts if a.id != account_id]
