# src/models/transaction.py
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.utils.database import Base
from src.models.account import Account
from src.models.category import Category
from src.models.user import User


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # "income" ou "expense"
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    account = relationship("Account", backref="transactions")
    category = relationship("Category", backref="transactions")
    user = relationship("User", backref="transactions")

    def __repr__(self):
        return (
            f"<Transaction(id={self.id}, amount={self.amount}, type='{self.type}', "
            f"account_id={self.account_id}, category_id={self.category_id}, "
            f"user_id={self.user_id})>"
        )
