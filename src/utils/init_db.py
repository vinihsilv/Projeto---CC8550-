# src/init_db.py
from src.utils.database import Base, engine
from src.models.user import User
from src.models.account import Account
from src.models.category import Category
from src.models.budget import Budget
from src.models.transaction import Transaction

# Cria todas as tabelas no banco
Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")
