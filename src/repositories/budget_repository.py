from sqlalchemy.orm import Session
from src.models.budget import Budget
from src.interfaces.budget_repository_interface import BudgetRepositoryInterface


class BudgetRepository(BudgetRepositoryInterface):
    """SQLAlchemy implementation of BudgetRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, budget: Budget) -> None:
        self.session.add(budget)
        self.session.commit()
        self.session.refresh(budget)

    def list(self) -> list[Budget]:
        return self.session.query(Budget).all()

    def get(self, budget_id: int) -> Budget | None:
        return self.session.query(Budget).filter_by(id=budget_id).first()

    def update(self, budget_id: int, data: dict) -> None:
        budget = self.get(budget_id)
        if not budget:
            raise ValueError("Budget not found")
        for key, value in data.items():
            if hasattr(budget, key):
                setattr(budget, key, value)
        self.session.commit()

    def delete(self, budget_id: int) -> None:
        budget = self.get(budget_id)
        if budget:
            self.session.delete(budget)
            self.session.commit()

    def list_by_category(self, category_id: int, user_id: int) -> Budget | None:
        return (
            self.session.query(Budget)
            .filter_by(category_id=category_id, user_id=user_id)
            .first()
        )
