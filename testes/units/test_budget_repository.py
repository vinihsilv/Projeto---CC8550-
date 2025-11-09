import sys
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# path para src
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.utils.database import Base
from src.models.user import User
from src.models.category import Category
from src.models.budget import Budget
from src.repositories.budget_repository import BudgetRepository


# ---------------- Fixtures locais ----------------


@pytest.fixture(scope="session")
def engine():
    eng = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)


@pytest.fixture(scope="function")
def session(engine):
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture
def sample_user(session):
    # gera email único para evitar violar UNIQUE
    import uuid

    email = f"tester_{uuid.uuid4().hex[:8]}@example.com"
    u = User(name="Tester", email=email, password="secret")
    session.add(u)
    session.commit()
    return u


@pytest.fixture
def sample_category(session, sample_user):
    c = Category(name="Marketing", user_id=sample_user.id)
    session.add(c)
    session.commit()
    return c


@pytest.fixture
def budget_repo(session):
    return BudgetRepository(session)


# ---------------- Testes ----------------


def test_create_budget(budget_repo, sample_user, sample_category):
    b = Budget(
        user_id=sample_user.id,
        category_id=sample_category.id,
        year=2025,
        month=11,
        limit_value=500.0,
    )
    budget_repo.create(b)
    assert b.id is not None
    got = budget_repo.get(b.id)
    assert got.limit_value == 500.0


def test_update_budget(budget_repo, sample_user, sample_category):
    b = Budget(
        user_id=sample_user.id,
        category_id=sample_category.id,
        year=2025,
        month=11,
        limit_value=500.0,
    )
    budget_repo.create(b)
    budget_repo.update(b.id, {"limit_value": 800.0, "month": 12})
    got = budget_repo.get(b.id)
    assert got.limit_value == 800.0
    assert got.month == 12


def test_update_budget_nonexistent(budget_repo):
    with pytest.raises(ValueError):
        budget_repo.update(9999, {"limit_value": 100.0})


def test_delete_budget(budget_repo, sample_user, sample_category):
    b = Budget(
        user_id=sample_user.id,
        category_id=sample_category.id,
        year=2025,
        month=11,
        limit_value=500.0,
    )
    budget_repo.create(b)
    budget_repo.delete(b.id)
    assert budget_repo.get(b.id) is None


def test_list_by_user(budget_repo, sample_user, sample_category):
    b1 = Budget(
        user_id=sample_user.id,
        category_id=sample_category.id,
        year=2025,
        month=11,
        limit_value=100.0,
    )
    b2 = Budget(
        user_id=sample_user.id,
        category_id=sample_category.id,
        year=2025,
        month=12,
        limit_value=200.0,
    )
    budget_repo.create(b1)
    budget_repo.create(b2)
    rows = budget_repo.list_by_user(sample_user.id)
    assert {r.id for r in rows} >= {b1.id, b2.id}


def test_list_by_category(budget_repo, sample_user, sample_category):
    b = Budget(
        user_id=sample_user.id,
        category_id=sample_category.id,
        year=2025,
        month=11,
        limit_value=300.0,
    )
    budget_repo.create(b)
    got = budget_repo.list_by_category(sample_category.id, sample_user.id)
    assert got is not None and got.id == b.id


@pytest.mark.parametrize("limit", [1.0, 50.5, 9999999.0])
def test_budget_limit_extremes(budget_repo, sample_user, sample_category, limit):
    b = Budget(
        user_id=sample_user.id,
        category_id=sample_category.id,
        year=2025,
        month=11,
        limit_value=limit,
    )
    budget_repo.create(b)
    got = budget_repo.get(b.id)
    assert got.limit_value == limit
