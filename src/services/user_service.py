from src.models.user import User
from src.repositories.user_repository import UserRepository


class UserService:
    """Handles business rules for user management."""

    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, name: str, email: str, password: str) -> None:
        existing_users = self.repository.list()
        if any(u.email == email for u in existing_users):
            raise ValueError("Email already exists.")

        next_id = 1 if not existing_users else max(u.id for u in existing_users) + 1
        user = User(id=next_id, name=name, email=email, password=password)
        self.repository.create(user)

    def list_users(self):
        return self.repository.list()

    def update_user(self, user_id: int, data: dict) -> None:
        # Business rule: user must exist
        users = self.repository.list()
        if not any(u.id == user_id for u in users):
            raise ValueError("User not found.")

        self.repository.update(user_id, data)

    def delete_user(self, user_id: int) -> None:
        users = self.repository.list()
        if not any(u.id == user_id for u in users):
            raise ValueError("User not found.")

        self.repository.delete(user_id)
