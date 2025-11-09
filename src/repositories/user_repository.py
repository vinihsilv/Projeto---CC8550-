from sqlalchemy.orm import Session
from src.models.user import User
from src.interfaces.user_repository_interface import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    """SQLAlchemy implementation of UserRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)  # atualiza o id gerado

    def list(self) -> list[User]:
        return self.session.query(User).all()

    def update(self, id: int, data: dict) -> None:
        user = self.session.query(User).filter_by(id=id).first()
        if not user:
            return
        user.name = data.get("name", user.name)
        user.email = data.get("email", user.email)
        user.password = data.get("password", user.password)
        self.session.commit()

    def delete(self, id: int) -> None:
        user = self.session.query(User).filter_by(id=id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
