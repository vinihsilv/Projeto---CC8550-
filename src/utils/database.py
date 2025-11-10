# src/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Caminho do arquivo SQLite
DATABASE_URL = "sqlite:///db.sqlite"

# Cria o engine do SQLAlchemy
# Controle de verbosidade do SQLAlchemy via variável de ambiente (padrão: False)
# Defina SQL_ECHO=true para habilitar logs de SQL quando precisar debugar.
SQL_ECHO = os.getenv("SQL_ECHO", "false").strip().lower() in {"1", "true", "yes", "on"}

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # necessário para SQLite
    echo=SQL_ECHO,  # por padrão não imprime, habilite com SQL_ECHO=true
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
