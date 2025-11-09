# src/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Caminho do arquivo SQLite
DATABASE_URL = "sqlite:///db.sqlite"

# Cria o engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # necessário para SQLite
    echo=True,  # mostra logs SQL no console, opcional
)

# Cria uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para herança dos models
Base = declarative_base()


# Função helper para usar a sessão com context manager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
