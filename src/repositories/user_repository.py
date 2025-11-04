from typing import List
from src.models.user import User
from src.interfaces.user_repository_interface import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    """Implements an in-memory user repository."""

    def __init__(self):
        self._users: List[User] = []

    def create(self, user: User) -> None:
        user.id = len(self._users) + 1
        self._users.append(user)

    def list(self) -> List[User]:
        return self._users

    def update(self, id: int, data: dict) -> None:
        for u in self._users:
            if u.id == id:
                u.name = data.get("name", u.name)
                u.email = data.get("email", u.email)
                u.password = data.get("password", u.password)

    def delete(self, id: int) -> None:
        self._users = [u for u in self._users if u.id != id]
