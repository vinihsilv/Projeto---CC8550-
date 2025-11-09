# src/controllers/account_controller.py
from src.services.account_service import AccountService


class AccountController:
    def __init__(self):
        self.service = AccountService()

    def create_account(self, user_id: int, name: str, balance: float):
        self.service.create_account(user_id, name, balance)

    def list_accounts(self, user_id: int):
        accounts = self.service.list_accounts(user_id)
        if not accounts:
            print("Nenhuma conta cadastrada.")
        for a in accounts:
            print(f"ID: {a.id}, Nome: {a.name}, Saldo: {a.balance}")

    def update_account(
        self, account_id: int, name: str | None = None, balance: float | None = None
    ):
        self.service.update_account(account_id, name, balance)

    def delete_account(self, account_id: int):
        self.service.delete_account(account_id)
