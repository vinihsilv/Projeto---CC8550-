# src/models/budget.py
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.models.user import User
from src.utils.database import Base
from src.models.category import Category


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    limit_value = Column(Float, nullable=False)

    user = relationship("User", backref="budgets")
    category = relationship("Category", backref="budgets")

    def __repr__(self):
        return (
            f"<Budget(id={self.id}, category_id={self.category_id}, month={self.month}, "
            f"year={self.year}, limit_value={self.limit_value}, user_id={self.user_id})>"
        )
