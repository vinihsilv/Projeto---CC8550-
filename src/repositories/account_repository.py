# src/repositories/account_repository.py
from sqlalchemy.orm import Session
from src.models.account import Account
from src.interfaces.account_repository_interface import AccountRepositoryInterface


class AccountRepository(AccountRepositoryInterface):
    """SQLAlchemy implementation of AccountRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, account: Account) -> None:
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)  # garante que o id seja atualizado

    def list(self) -> list[Account]:
        return self.session.query(Account).all()

    def get(self, account_id: int) -> Account | None:
        return self.session.query(Account).filter_by(id=account_id).first()

    def update(self, account_id: int, data: dict) -> None:
        account = self.get(account_id)
        if not account:
            raise ValueError(f"Conta com id {account_id} não encontrada")
        for key, value in data.items():
            if hasattr(account, key):
                setattr(account, key, value)
            else:
                raise ValueError(f"Atributo '{key}' não existe na Account")
        self.session.commit()

    def list_by_user(self, user_id: int):
        return (
            self.session.query(Account)
            .filter(Account.user_id == user_id)
            .order_by(Account.id.asc())
            .all()
        )

    def delete(self, account_id: int) -> None:
        account = self.get(account_id)
        if account:
            self.session.delete(account)
            self.session.commit()
