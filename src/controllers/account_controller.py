# src/controllers/account_controller.py
from src.services.account_service import AccountService
from src.repositories.account_repository import AccountRepository


class AccountController:
    def __init__(self):
        repo = AccountRepository()
        self.service = AccountService(repo)

    def create_account(self, name, user_id):
        self.service.create_account(name, user_id)

    def list_accounts(self, user_id):
        return self.service.list_accounts(user_id)

    def get_account(self, account_id):
        return self.service.get_account(account_id)

    def update_account(self, account_id, data):
        self.service.update_account(account_id, data)

    def delete_account(self, account_id):
        self.service.delete_account(account_id)
