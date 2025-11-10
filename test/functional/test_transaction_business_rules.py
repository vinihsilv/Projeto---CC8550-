import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.utils.database import Base
from src.repositories.user_repository import UserRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.account_repository import AccountRepository
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.budget_repository import BudgetRepository

from src.controllers.user_controller import UserController
from src.controllers.category_controller import CategoryController
from src.controllers.account_controller import AccountController
from src.controllers.transaction_controller import TransactionController


# ------- Infra fixtures (acceptance style using real repos over in-memory DB) -------


@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    yield s
    s.close()


@pytest.fixture
def controllers(session):
    user_repo = UserRepository(session)
    category_repo = CategoryRepository(session)
    account_repo = AccountRepository(session)
    transaction_repo = TransactionRepository(session)
    budget_repo = BudgetRepository(session)

    return {
        "user": UserController(user_repo),
        "category": CategoryController(category_repo),
        "account": AccountController(account_repo),
        "transaction": TransactionController(
            transaction_repo, account_repo, category_repo, budget_repo
        ),
    }


@pytest.fixture
def user(controllers):
    return controllers["user"].create_user("Alice", "alice@example.com", "secret")


# ------- Acceptance tests for business rules -------


def test_cannot_create_transaction_without_category(session, controllers, user):
    """
    Regra: Não deve ser possível criar transação sem categoria válida.
    Cenário: Conta existe, categoria é None (ou inexistente) -> ValueError esperado.
    """
    # Dado uma conta válida do usuário
    # Nota: AccountController.create_account não retorna a conta criada,
    # então buscamos após criar.
    controllers["account"].create_account("Conta Corrente", user.id)
    accounts = controllers["account"].list_accounts(user.id)
    assert accounts, "Conta não foi criada corretamente para o usuário"
    # Seleciona a conta recém-criada (pode ser a única neste teste)
    account = next((a for a in accounts if a.name == "Conta Corrente"), accounts[0])

    # Quando tento criar transação sem categoria (category_id=None)
    with pytest.raises(ValueError, match=r"Categoria não encontrada: id=None"):
        controllers["transaction"].create_transaction(
            user_id=user.id,
            amount=50.0,
            type_="expense",
            account_id=account.id,
            category_id=None,  # categoria ausente
            description="Compra sem categoria",
        )

    # E quando tento com categoria inexistente (ex.: 999)
    with pytest.raises(ValueError, match=r"Categoria não encontrada: id=999"):
        controllers["transaction"].create_transaction(
            user_id=user.id,
            amount=50.0,
            type_="expense",
            account_id=account.id,
            category_id=999,  # categoria inexistente
            description="Compra categoria inválida",
        )


def test_cannot_create_transaction_without_account(session, controllers, user):
    """
    Regra: Não deve ser possível criar transação sem conta válida.
    Cenário: Categoria existe, conta é None (ou inexistente) -> ValueError esperado.
    """
    # Dado uma categoria válida do usuário
    category = controllers["category"].create_category("Alimentação", user.id)

    # Quando tento criar transação sem conta (account_id=None)
    with pytest.raises(ValueError, match=r"Conta não encontrada: id=None"):
        controllers["transaction"].create_transaction(
            user_id=user.id,
            amount=80.0,
            type_="expense",
            account_id=None,  # conta ausente
            category_id=category.id,
            description="Compra sem conta",
        )

    # E quando tento com conta inexistente (ex.: 999)
    with pytest.raises(ValueError, match=r"Conta não encontrada: id=999"):
        controllers["transaction"].create_transaction(
            user_id=user.id,
            amount=80.0,
            type_="expense",
            account_id=999,  # conta inexistente
            category_id=category.id,
            description="Compra conta inválida",
        )
