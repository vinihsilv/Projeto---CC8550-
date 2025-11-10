import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.utils.database import Base
from src.models.transaction import Transaction
from src.models.account import Account
from src.models.category import Category
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.account_repository import AccountRepository
from src.repositories.category_repository import CategoryRepository


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
def sample_account(account_repo):
    acc = Account(id=None, name="Conta Performance Test", balance=10000, user_id=1)
    account_repo.create(acc)
    return acc


@pytest.fixture
def sample_category(category_repo):
    cat = Category(id=None, name="Categoria Performance Test", user_id=1)
    category_repo.create(cat)
    return cat


# --- Performance Tests ---


@pytest.mark.benchmark(group="transaction")
def test_large_transaction_batch(
    benchmark, transaction_repo, sample_account, sample_category
):
    """Testa a performance de criação em lote de transações."""

    def create_transactions():
        for i in range(1000):  # simula grande volume
            transaction_repo.create(
                Transaction(
                    account_id=sample_account.id,
                    category_id=sample_category.id,
                    amount=float(i),
                    description=f"Teste carga {i}",
                    type="expense" if i % 2 == 0 else "income",
                    user_id=1,
                )
            )

    benchmark(create_transactions)


@pytest.mark.benchmark(group="transaction")
def test_transaction_retrieval_performance(
    benchmark, transaction_repo, sample_account, sample_category
):
    """Testa a performance de recuperação de transações."""
    # Primeiro, criar algumas transações para testar
    for i in range(100):
        transaction_repo.create(
            Transaction(
                account_id=sample_account.id,
                category_id=sample_category.id,
                amount=float(i * 10),
                description=f"Setup transaction {i}",
                type="expense" if i % 2 == 0 else "income",
                user_id=1,
            )
        )

    def retrieve_transactions():
        return transaction_repo.list_by_user(1)

    benchmark(retrieve_transactions)


@pytest.mark.benchmark(group="transaction")
def test_transaction_update_performance(
    benchmark, transaction_repo, sample_account, sample_category
):
    """Testa a performance de atualização de transações."""
    # Criar transações para teste
    transactions = []
    for i in range(50):
        tx = transaction_repo.create(
            Transaction(
                account_id=sample_account.id,
                category_id=sample_category.id,
                amount=float(i * 5),
                description=f"Update test {i}",
                type="expense",
                user_id=1,
            )
        )
        transactions.append(tx)

    def update_transactions():
        for tx in transactions:
            transaction_repo.update(
                tx.id,
                {"amount": tx.amount * 2, "description": f"Updated {tx.description}"},
            )

    benchmark(update_transactions)


@pytest.mark.benchmark(group="transaction")
def test_transaction_deletion_performance(
    benchmark, transaction_repo, sample_account, sample_category
):
    """Testa a performance de deleção de transações."""
    # Criar transações para teste
    transaction_ids = []
    for i in range(100):
        tx = transaction_repo.create(
            Transaction(
                account_id=sample_account.id,
                category_id=sample_category.id,
                amount=float(i * 10),
                description=f"Delete test {i}",
                type="expense" if i % 2 == 0 else "income",
                user_id=1,
            )
        )
        transaction_ids.append(tx.id)

    def delete_transactions():
        for tx_id in transaction_ids:
            transaction_repo.delete(tx_id)

    benchmark(delete_transactions)


@pytest.mark.benchmark(group="query")
def test_transaction_by_account_performance(
    benchmark, transaction_repo, sample_account, sample_category
):
    """Testa a performance de consultas por conta."""
    # Criar transações para teste
    for i in range(200):
        transaction_repo.create(
            Transaction(
                account_id=sample_account.id,
                category_id=sample_category.id,
                amount=float(i * 15),
                description=f"Account query test {i}",
                type="expense" if i % 2 == 0 else "income",
                user_id=1,
            )
        )

    def query_by_account():
        return transaction_repo.list_by_account(sample_account.id)

    benchmark(query_by_account)


@pytest.mark.benchmark(group="query")
def test_transaction_by_category_performance(
    benchmark, transaction_repo, sample_account, sample_category
):
    """Testa a performance de consultas por categoria."""
    # Criar transações para teste
    for i in range(150):
        transaction_repo.create(
            Transaction(
                account_id=sample_account.id,
                category_id=sample_category.id,
                amount=float(i * 8),
                description=f"Category query test {i}",
                type="expense" if i % 3 == 0 else "income",
                user_id=1,
            )
        )

    def query_by_category():
        return transaction_repo.list_by_category(sample_category.id, user_id=1)

    benchmark(query_by_category)
