from abc import ABC, abstractmethod
from typing import List
from src.models.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def create(self, user: User) -> None:
        pass

    @abstractmethod
    def list(self) -> List[User]:
        pass

    @abstractmethod
    def update(self, id: int, data: dict) -> None:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
