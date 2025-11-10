import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.utils.database import Base
from src.models.transaction import Transaction
from src.models.account import Account
from src.models.category import Category
from src.models.budget import Budget
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.account_repository import AccountRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.budget_repository import BudgetRepository

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
def account_repo(session):
    return AccountRepository(session)


@pytest.fixture
def category_repo(session):
    return CategoryRepository(session)


@pytest.fixture
def transaction_repo(session):
    return TransactionRepository(session)


@pytest.fixture
def budget_repo(session):
    return BudgetRepository(session)


@pytest.fixture
def sample_account(account_repo):
    acc = Account(
        id=None, name="Conta Teste", balance=1000, user_id=1
    )  # <-- adicionado user_id
    account_repo.create(acc)
    return acc


@pytest.fixture
def sample_category(category_repo):
    cat = Category(id=None, name="Categoria Teste", user_id=1)
    category_repo.create(cat)
    return cat


# --- TransactionRepository Tests ---


def test_create_transaction(transaction_repo, sample_account, sample_category):
    tx = Transaction(
        id=None,
        account_id=sample_account.id,
        category_id=sample_category.id,
        amount=200.0,
        description="Pagamento",
        type="credit",  # <-- obrigatório
        user_id=1,  # <-- se a tabela exigir
    )
    transaction_repo.create(tx)
    assert tx.id is not None


def test_update_transaction(transaction_repo, sample_account, sample_category):
    tx = Transaction(
        id=None,
        account_id=sample_account.id,
        category_id=sample_category.id,
        amount=200,
        description="Pagamento",
        type="debit",
        user_id=1,
    )
    transaction_repo.create(tx)
    transaction_repo.update(tx.id, {"amount": 300, "description": "Atualizado"})
    updated = transaction_repo.session.query(Transaction).get(tx.id)
    assert updated.amount == 300
    assert updated.description == "Atualizado"


def test_update_nonexistent_transaction(transaction_repo):
    # apenas não faz nada
    transaction_repo.update(999, {"amount": 100})
    # garante que não levantou erro
    assert True


def test_delete_transaction(transaction_repo, sample_account, sample_category):
    tx = Transaction(
        id=None,
        account_id=sample_account.id,
        category_id=sample_category.id,
        amount=200,
        description="Pagamento",
        type="debit",
        user_id=1,
    )
    transaction_repo.create(tx)
    transaction_repo.delete(tx.id)
    assert transaction_repo.session.query(Transaction).get(tx.id) is None


@pytest.mark.parametrize("amount", [0, -50, 999999])
def test_transaction_extremes(
    transaction_repo, sample_account, sample_category, amount
):
    tx = Transaction(
        id=None,
        account_id=sample_account.id,
        category_id=sample_category.id,
        amount=amount,
        description="Teste extremo",
        type="debit",  # obrigatório
        user_id=sample_account.user_id,  # obrigatório
    )
    transaction_repo.create(tx)
    fetched = transaction_repo.get_by_id(tx.id)
    assert fetched.amount == amount
