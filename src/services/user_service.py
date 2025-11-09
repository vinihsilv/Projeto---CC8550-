from typing import List
from src.models.user import User
from src.repositories.user_repository import UserRepositoryInterface
from sqlalchemy.exc import IntegrityError


class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def create_user(self, name: str, email: str, password: str) -> User:
        # Verifica se email já existe
        existing_user = (
            self.repository.session.query(User).filter_by(email=email).first()
        )
        if existing_user:
            raise ValueError("Email already exists.")

        user = User(id=None, name=name, email=email, password=password)
        self.repository.create(user)
        return user

    def list_users(self) -> List[User]:
        return self.repository.list()

    def authenticate(self, email: str, password: str) -> User | None:
        return (
            self.repository.session.query(User)
            .filter_by(email=email, password=password)
            .first()
        )

    def get_user(self, user_id: int) -> User:
        user = self.repository.session.query(User).filter_by(id=user_id).first()
        if not user:
            raise ValueError("User not found.")
        return user

    def update_user(self, user_id: int, data: dict) -> None:
        user = self.get_user(user_id)
        self.repository.update(user_id, data)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.repository.delete(user_id)
