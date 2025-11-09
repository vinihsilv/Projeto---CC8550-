# src/services/user_service.py
from typing import List
from src.models.user import User
from src.repositories.user_repository import UserRepositoryInterface


class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def create_user(self, name: str, email: str, password: str) -> None:
        if any(u.email == email for u in self.repository.list()):
            raise ValueError("Email already exists.")
        next_id = (
            1
            if not self.repository.list()
            else max(u.id for u in self.repository.list()) + 1
        )
        self.repository.create(
            User(id=next_id, name=name, email=email, password=password)
        )

    def list_users(self) -> List[User]:
        return self.repository.list()

    def authenticate(self, email: str, password: str) -> User | None:
        users = self.repository.list()
        for u in users:
            if u.email == email and u.password == password:
                return u
        return None

    def get_user(self, user_id: int) -> User:
        user = self.repository.get(user_id)
        if not user:
            raise ValueError("User not found.")
        return user

    def update_user(self, user_id: int, data: dict) -> None:
        user = self.get_user(user_id)
        self.repository.update(user_id, data)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.repository.delete(user_id)
