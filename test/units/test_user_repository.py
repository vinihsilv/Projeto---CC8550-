import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.utils.database import Base
from src.models.user import User
from src.repositories.user_repository import UserRepository


# --- Fixtures ---


@pytest.fixture(scope="function")
def session():
    """Cria um banco SQLite em memória para cada teste."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def repo(session):
    """Retorna um UserRepository com a sessão de teste."""
    return UserRepository(session)


# --- Testes ---


def test_create_user(repo):
    user = User(id=None, name="Alice", email="alice@example.com", password="123")
    repo.create(user)
    assert user.id is not None
    db_user = repo.get(user.id)
    assert db_user.email == "alice@example.com"


def test_list_users(repo):
    user1 = User(id=None, name="Alice", email="alice@example.com", password="123")
    user2 = User(id=None, name="Bob", email="bob@example.com", password="456")
    repo.create(user1)
    repo.create(user2)
    users = repo.list()
    assert len(users) == 2
    emails = [u.email for u in users]
    assert "alice@example.com" in emails and "bob@example.com" in emails


def test_get_nonexistent_user(repo):
    user = repo.get(999)
    assert user is None


def test_update_user(repo):
    user = User(id=None, name="Alice", email="alice@example.com", password="123")
    repo.create(user)
    repo.update(user.id, {"name": "Alice Updated"})
    updated = repo.get(user.id)
    assert updated.name == "Alice Updated"


def test_update_nonexistent_user(repo):
    with pytest.raises(ValueError):
        repo.update(999, {"name": "No One"})


def test_delete_user(repo):
    user = User(id=None, name="Alice", email="alice@example.com", password="123")
    repo.create(user)
    repo.delete(user.id)
    assert repo.get(user.id) is None


def test_delete_nonexistent_user(repo):
    # Deve apenas não fazer nada, sem levantar erro
    repo.delete(999)
    assert repo.get(999) is None


def test_unique_email_constraint(repo):
    user1 = User(id=None, name="Alice", email="alice@example.com", password="123")
    user2 = User(id=None, name="Alice2", email="alice@example.com", password="456")
    repo.create(user1)
    # Inserir email duplicado deve falhar no banco
    with pytest.raises(Exception):
        repo.create(user2)
