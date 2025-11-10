import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.utils.database import Base
from src.models.account import Account
from src.repositories.account_repository import AccountRepository

# --- Fixtures ---


@pytest.fixture(scope="function")
def session():
    """Cria um banco SQLite em memória para cada teste."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def repo(session):
    """Retorna um AccountRepository com a sessão de teste."""
    return AccountRepository(session)


@pytest.fixture
def sample_accounts(repo):
    acc1 = Account(id=None, name="Conta1", balance=100, user_id=1)
    acc2 = Account(id=None, name="Conta2", balance=200, user_id=1)
    repo.create(acc1)
    repo.create(acc2)
    return [acc1, acc2]


# --- Testes ---


def test_create_account(repo):
    acc = Account(id=None, name="Conta3", balance=50, user_id=2)
    repo.create(acc)
    assert acc.id is not None
    db_acc = repo.session.query(Account).filter_by(id=acc.id).first()
    assert db_acc.name == "Conta3"


def test_list_accounts(repo, sample_accounts):
    accounts = repo.list()
    assert len(accounts) == 2
    names = [a.name for a in accounts]
    assert "Conta1" in names and "Conta2" in names


def test_get_existing_account(repo, sample_accounts):
    acc_id = sample_accounts[0].id
    acc = repo.get(acc_id)
    assert acc.name == "Conta1"


def test_get_nonexistent_account(repo):
    acc = repo.get(999)
    assert acc is None


def test_update_account(repo, sample_accounts):
    acc_id = sample_accounts[0].id
    repo.update(acc_id, {"name": "Conta1 Updated", "balance": 500})
    updated = repo.get(acc_id)
    assert updated.name == "Conta1 Updated"
    assert updated.balance == 500


def test_update_nonexistent_account(repo):
    with pytest.raises(ValueError):
        repo.update(999, {"name": "Inexistente", "balance": 0})


def test_delete_account(repo, sample_accounts):
    acc_id = sample_accounts[0].id
    repo.delete(acc_id)
    assert repo.get(acc_id) is None


def test_delete_nonexistent_account(repo):
    # Não deve lançar erro
    repo.delete(999)
    assert repo.list() == []


# --- Casos extremos e parametrização ---


@pytest.mark.parametrize(
    "name,balance",
    [
        ("", 0),  # nome vazio, saldo zero
        ("Conta Extrema", -1000),  # saldo negativo
        ("C" * 300, 999999999),  # nome longo, saldo muito grande
    ],
)
def test_create_account_extremes(repo, name, balance):
    acc = Account(id=None, name=name, balance=balance, user_id=1)
    repo.create(acc)
    db_acc = repo.get(acc.id)
    assert db_acc.name == name
    assert db_acc.balance == balance
