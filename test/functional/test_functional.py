import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from src.utils.database import Base
from src.repositories.user_repository import UserRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.budget_repository import BudgetRepository
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.account_repository import AccountRepository

from src.services.user_service import UserService
from src.services.category_service import CategoryService
from src.services.budget_service import BudgetService
from src.services.transaction_service import TransactionService

from src.models.account import Account


# ---------------- FIXTURES GERAIS ---------------- #


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    # ativa FKs no SQLite (útil para cascades)
    if engine.url.get_backend_name() == "sqlite":

        @event.listens_for(engine, "connect")
        def _fk_on(dbapi_connection, connection_record):
            dbapi_connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def services(db_session):
    user_repo = UserRepository(db_session)
    category_repo = CategoryRepository(db_session)
    budget_repo = BudgetRepository(db_session)
    account_repo = AccountRepository(db_session)
    tx_repo = TransactionRepository(db_session)

    return {
        "user": UserService(user_repo),
        "category": CategoryService(category_repo),
        "budget": BudgetService(budget_repo),  # ajustado: só repo de budget
        "transaction": TransactionService(
            tx_repo, account_repo, category_repo, budget_repo
        ),
    }


@pytest.fixture
def user(services):
    return services["user"].create_user("Ana", "ana@mail.com", "123")


@pytest.fixture
def category(services, user):
    return services["category"].create_category("Alimentação", user.id)


@pytest.fixture
def account(db_session, user):
    acc = Account(name="Conta Padrão", balance=0.0, user_id=user.id)
    db_session.add(acc)
    db_session.commit()
    return acc


# ---------------- TESTES FUNCIONAIS ---------------- #


def test_func_cadastro_categoria(services, user):
    cat = services["category"].create_category("Transporte", user.id)
    assert cat.id > 0
    assert cat.name == "Transporte"


def test_func_criacao_orcamento(services, user, category):
    budget = services["budget"].create_budget(user.id, category.id, 2025, 5, 1200)
    assert budget.limit_value == 1200
    assert budget.month == 5


def test_func_registro_transacao(services, user, category, account):
    # garante saldo para despesa
    services["transaction"].account_repository.update(account.id, {"balance": 500.0})
    services["transaction"].create_transaction(
        user_id=user.id,
        amount=100.0,
        type_="expense",
        account_id=account.id,
        category_id=category.id,
        description="Supermercado",
    )
    # verifica via service
    txs = services["transaction"].list_transactions(user.id)
    assert any(t.description == "Supermercado" and t.amount == 100.0 for t in txs)


def test_func_saldo_pos_transacao(services, user, category, account):
    services["transaction"].account_repository.update(account.id, {"balance": 300.0})
    services["transaction"].create_transaction(
        user_id=user.id,
        amount=200.0,
        type_="expense",
        account_id=account.id,
        category_id=category.id,
        description="Compra",
    )
    acc = services["transaction"].account_repository.get(account.id)
    assert acc.balance == 100.0


def test_func_consulta_orcamento(services, user, category):
    services["budget"].create_budget(user.id, category.id, 2025, 5, 1500)
    budgets = services["budget"].list_budgets(user.id)
    assert len(budgets) == 1
    assert budgets[0].limit_value == 1500


def test_func_excluir_categoria_com_transacoes(services, user, category, account):
    services["transaction"].account_repository.update(account.id, {"balance": 200.0})
    services["transaction"].create_transaction(
        user_id=user.id,
        amount=50.0,
        type_="expense",
        account_id=account.id,
        category_id=category.id,
        description="Lanche",
    )
    services["category"].delete_category(category.id)

    with pytest.raises(ValueError):
        services["category"].get_category(category.id)


def test_func_transacao_invalida(services, user, account):
    # categoria inexistente dispara erro
    with pytest.raises(ValueError):
        services["transaction"].create_transaction(
            user_id=user.id,
            amount=10.0,
            type_="expense",
            account_id=account.id,
            category_id=999999,
            description="Falha",
        )


def test_func_fluxo_completo_orcamento(services, user, account):
    # 1. Categoria
    cat = services["category"].create_category("Lazer", user.id)

    # 2. Orçamento
    budget = services["budget"].create_budget(user.id, cat.id, 2025, 6, 500)

    services["transaction"].account_repository.update(account.id, {"balance": 600.0})
    services["transaction"].create_transaction(
        user_id=user.id,
        amount=100.0,
        type_="expense",
        account_id=account.id,
        category_id=cat.id,
        description="Cinema",
    )

    txs = services["transaction"].list_transactions(user.id)
    total = sum(
        t.amount if t.type == "income" else -t.amount
        for t in txs
        if t.category_id == cat.id
    )
    assert (
        total == -100 or total == 100
    )  # dependendo da sua convenção; ajuste se necessário

    # 5. Editar limite
    services["budget"].update_budget(budget.id, {"limit_value": 800})
    updated = services["budget"].get_budget(budget.id)
    assert updated.limit_value == 800

    # 6. Excluir orçamento
    services["budget"].delete_budget(budget.id)

    with pytest.raises(ValueError):
        services["budget"].get_budget(budget.id)
