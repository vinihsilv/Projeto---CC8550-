# src/controllers/user_controller.py
from src.models.user import User
from src.services.user_service import UserService
from src.repositories.user_repository import UserRepository
from src.utils.database import SessionLocal


class UserController:
    def __init__(self, repo: UserRepository):
        self.service = UserService(repo)

    def create_user(self, name: str, email: str, password: str) -> User:
        return self.service.create_user(name, email, password)

    def list_users(self) -> list[User]:
        return self.service.list_users()

    def login(self, email: str, password: str) -> User | None:
        return self.service.authenticate(email, password)

    def get_user(self, user_id: int) -> User:
        return self.service.get_user(user_id)

    def update_user(self, user_id: int, data: dict) -> None:
        self.service.update_user(user_id, data)

    def delete_user(self, user_id: int) -> None:
        self.service.delete_user(user_id)
