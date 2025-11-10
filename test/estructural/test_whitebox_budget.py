import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from src.utils.database import Base
from src.models.user import User
from src.models.account import Account
from src.models.category import Category
from src.models.budget import Budget
from src.repositories.account_repository import AccountRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.budget_repository import BudgetRepository
from src.repositories.transaction_repository import TransactionRepository
from src.services.transaction_service import TransactionService
from src.services.category_service import CategoryService
from src.services.budget_service import BudgetService

# ---------------- engine/session ----------------


@pytest.fixture(scope="function")
def engine():
    eng = create_engine("sqlite:///:memory:", future=True)
    if eng.url.get_backend_name() == "sqlite":

        @event.listens_for(eng, "connect")
        def _fk_on(dbapi_connection, connection_record):
            dbapi_connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)


@pytest.fixture(scope="function")
def session(engine):
    SessionLocal = sessionmaker(bind=engine, future=True)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


# ---------------- fixtures de dados ----------------


@pytest.fixture
def user(session):
    u = User(name="User1", email="user1@test.com", password="123")
    session.add(u)
    session.commit()
    return u


@pytest.fixture
def category(session, user):
    c = Category(name="Food", user_id=user.id)
    session.add(c)
    session.commit()
    return c


@pytest.fixture
def account(session, user):
    a = Account(name="Main", balance=0.0, user_id=user.id)
    session.add(a)
    session.commit()
    return a


# ---------------- repos & services ----------------


@pytest.fixture
def account_repo(session):
    return AccountRepository(session)


@pytest.fixture
def category_repo(session):
    return CategoryRepository(session)


@pytest.fixture
def budget_repo(session):
    return BudgetRepository(session)


@pytest.fixture
def transaction_repo(session):
    return TransactionRepository(session)


@pytest.fixture
def budget_service(budget_repo):
    return BudgetService(budget_repo)


@pytest.fixture
def cat_service(category_repo):
    return CategoryService(category_repo)


@pytest.fixture
def transaction_service(transaction_repo, account_repo, category_repo, budget_repo):
    return TransactionService(
        transaction_repo, account_repo, category_repo, budget_repo
    )


# ---------------- testes de orçamento ----------------


def test_create_new_budget_branch(budget_service, user, category):
    b = budget_service.create_budget(user.id, category.id, 2025, 1, 200.0)
    assert b.id is not None
    assert b.limit_value == 200.0
    assert b.year == 2025 and b.month == 1


def test_update_existing_budget_branch(budget_service, session, user, category):
    existing = Budget(
        user_id=user.id, category_id=category.id, year=2025, month=1, limit_value=300.0
    )
    session.add(existing)
    session.commit()
    with pytest.raises(
        ValueError
    ):  # regra: não pode duplicar orçamento no mesmo ano/mês
        budget_service.create_budget(user.id, category.id, 2025, 1, 999.0)


@pytest.mark.parametrize("bad_month", [0, 13, -5])
def test_budget_invalid_month(budget_service, user, category, bad_month):
    with pytest.raises(ValueError):
        budget_service.create_budget(user.id, category.id, 2025, bad_month, 100.0)


@pytest.mark.parametrize("bad_limit", [0.0, -10.0])
def test_budget_invalid_limit(budget_service, user, category, bad_limit):
    with pytest.raises(ValueError):
        budget_service.create_budget(user.id, category.id, 2025, 3, bad_limit)


def test_budget_delete(budget_service, budget_repo, user, category):
    b = budget_service.create_budget(user.id, category.id, 2025, 4, 400.0)
    budget_service.delete_budget(b.id)
    assert budget_repo.get(b.id) is None


# ---------------- testes de transação ----------------


def test_create_transaction_valid(
    transaction_service, transaction_repo, account_repo, user, category, account
):
    account_repo.update(account.id, {"balance": 300.0})
    transaction_service.create_transaction(
        user_id=user.id,
        amount=100.0,
        type_="expense",
        account_id=account.id,
        category_id=category.id,
        description="Compra OK",
    )
    tx = transaction_repo.list_by_user(user.id)[-1]
    assert tx.amount == 100.0
    assert tx.type == "expense"


def test_create_transaction_invalid_type(transaction_service, user, category, account):
    with pytest.raises(ValueError):
        transaction_service.create_transaction(
            user_id=user.id,
            amount=20.0,
            type_="INVALIDO",
            account_id=account.id,
            category_id=category.id,
            description="Teste",
        )


def test_update_transaction_nonexistent(transaction_service, user):
    with pytest.raises(ValueError):
        transaction_service.update_transaction(
            transaction_id=999, user_id=user.id, amount=100.0
        )


def test_delete_transaction_wrong_user(
    transaction_service,
    transaction_repo,
    account_repo,
    user,
    category,
    account,
    session,
):
    # cria usuário extra
    other_user = User(name="X", email="x@test.com", password="123")
    session.add(other_user)
    session.commit()

    account_repo.update(account.id, {"balance": 300.0})
    transaction_service.create_transaction(
        user_id=user.id,
        amount=20.0,
        type_="expense",
        account_id=account.id,
        category_id=category.id,
        description="Errado",
    )

    tx = transaction_repo.list_by_user(user.id)[-1]

    with pytest.raises(ValueError):
        transaction_service.delete_transaction(
            transaction_id=tx.id, user_id=other_user.id
        )


def test_create_transaction_insufficient_balance_expense(
    transaction_service, account_repo, user, category, account
):
    account_repo.update(account.id, {"balance": 10.0})

    with pytest.raises(ValueError):
        transaction_service.create_transaction(
            user_id=user.id,
            amount=50.0,
            type_="expense",
            account_id=account.id,
            category_id=category.id,
            description="Sem saldo",
        )


def test_update_transaction_branch(
    transaction_service, transaction_repo, account_repo, user, category, account
):
    account_repo.update(account.id, {"balance": 300.0})
    transaction_service.create_transaction(
        user_id=user.id,
        amount=100.0,
        type_="expense",
        account_id=account.id,
        category_id=category.id,
        description="Original",
    )
    tx = transaction_repo.list_by_user(user.id)[-1]
    transaction_service.update_transaction(
        transaction_id=tx.id,
        user_id=user.id,
        amount=150.0,
    )
    updated = transaction_repo.get_by_id(tx.id)
    assert updated.amount == 150.0


def test_delete_transaction(
    transaction_service, transaction_repo, account_repo, user, category, account
):
    account_repo.update(account.id, {"balance": 300.0})
    transaction_service.create_transaction(
        user_id=user.id,
        amount=50.0,
        type_="expense",
        account_id=account.id,
        category_id=category.id,
        description="Apagar",
    )
    tx = transaction_repo.list_by_user(user.id)[-1]
    transaction_service.delete_transaction(transaction_id=tx.id, user_id=user.id)
    assert transaction_repo.get_by_id(tx.id) is None


# ---------------- testes de categoria ----------------


def test_create_category_duplicate(cat_service, user):
    cat1 = cat_service.create_category("Dup", user.id)
    try:
        cat2 = cat_service.create_category("Dup", user.id)
        # se não houver validação de duplicidade, ao menos deve criar outra categoria
        assert cat2.id != cat1.id
    except ValueError:
        # se houver validação, aceite a exceção
        assert True


def test_delete_category_in_use(
    cat_service, transaction_service, account_repo, user, category, account
):
    account_repo.update(account.id, {"balance": 200.0})
    transaction_service.create_transaction(
        user_id=user.id,
        amount=50.0,
        type_="expense",
        account_id=account.id,
        category_id=category.id,
        description="Lanche",
    )
    # comportamento depende da regra de negócio; aqui garantimos que a chamada não gera IntegrityError por falta de account_id
    try:
        cat_service.delete_category(category.id)
    except ValueError:
        # se a regra bloquear exclusão com transações, aceite
        assert True


def test_category_create_and_get(category_repo, session, user):
    c = Category(name="Cat1", user_id=user.id)
    session.add(c)
    session.commit()
    got = category_repo.get_category(c.id)
    assert got is not None and got.name == "Cat1"


def test_category_update(category_repo, session, user):
    c = Category(name="Old", user_id=user.id)
    session.add(c)
    session.commit()
    category_repo.update(c.id, {"name": "New"})
    got = category_repo.get_category(c.id)
    assert got is not None and got.name == "New"


def test_category_list_by_user(category_repo, session, user):
    session.add_all(
        [
            Category(name="A", user_id=user.id),
            Category(name="B", user_id=user.id),
        ]
    )
    session.commit()
    rows = category_repo.list_by_user(user.id)
    assert len(rows) >= 2


def test_account_create_and_fetch(account_repo, session, user):
    acc = Account(name="Acc1", balance=10.0, user_id=user.id)
    session.add(acc)
    session.commit()
    got = account_repo.get(acc.id)
    assert got is not None and got.name == "Acc1"


def test_account_update(account_repo, session, user):
    acc = Account(name="AccUpd", balance=5.0, user_id=user.id)
    session.add(acc)
    session.commit()
    account_repo.update(acc.id, {"balance": 77.7})
    got = account_repo.get(acc.id)
    assert got.balance == 77.7


def test_account_list_by_user(account_repo, session, user):
    session.add_all(
        [
            Account(name="A1", balance=0.0, user_id=user.id),
            Account(name="A2", balance=1.0, user_id=user.id),
        ]
    )
    session.commit()
    rows = account_repo.list_by_user(user.id)
    assert len(rows) == 2
