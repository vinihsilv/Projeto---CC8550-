import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.utils.database import Base
from src.models.category import Category
from src.repositories.category_repository import CategoryRepository


# ---------------- Fixtures ----------------


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
    """Retorna um CategoryRepository com a sessão de teste."""
    return CategoryRepository(session)


@pytest.fixture
def sample_categories(repo):
    """Cria categorias de teste."""
    c1 = Category(id=None, name="Alimentação", user_id=1)
    c2 = Category(id=None, name="Transporte", user_id=1)
    repo.create(c1)
    repo.create(c2)
    return [c1, c2]


# ---------------- Testes ----------------


def test_create_category(repo):
    cat = Category(id=None, name="Saúde", user_id=2)
    repo.create(cat)
    assert cat.id is not None
    db_cat = repo.session.query(Category).filter_by(id=cat.id).first()
    assert db_cat.name == "Saúde"


def test_list_categories(repo, sample_categories):
    categories = repo.list_all()
    assert len(categories) == 2

    names = [c.name for c in categories]
    assert "Alimentação" in names
    assert "Transporte" in names


def test_get_category(repo, sample_categories):
    cat_id = sample_categories[0].id
    cat = repo.get(cat_id)
    assert cat.name == "Alimentação"


def test_get_nonexistent_category(repo):
    cat = repo.get(999)
    assert cat is None


def test_update_category(repo, sample_categories):
    cat_id = sample_categories[0].id
    repo.update(cat_id, {"name": "Comida"})
    updated = repo.get(cat_id)
    assert updated.name == "Comida"


def test_update_nonexistent_category(repo):
    # Deve não fazer nada, sem erro
    repo.update(999, {"name": "Inexistente"})
    cat = repo.get(999)
    assert cat is None


def test_delete_category(repo, sample_categories):
    cat_id = sample_categories[1].id
    repo.delete(cat_id)
    assert repo.get(cat_id) is None
    remaining = repo.list_all()
    assert len(remaining) == 1


def test_delete_nonexistent_category(repo):
    # Não deve levantar erro
    repo.delete(999)
    assert repo.list_all() == []


@pytest.mark.parametrize(
    "name,user_id",
    [
        ("Entretenimento", 1),
        ("", 1),  # string vazia
        ("x" * 300, 2),  # string muito longa
    ],
)
def test_create_category_extremes(repo, name, user_id):
    cat = Category(id=None, name=name, user_id=user_id)
    repo.create(cat)
    db_cat = repo.get(cat.id)
    assert db_cat.name == name
    assert db_cat.user_id == user_id


def test_list_by_user(repo, sample_categories):
    # Adiciona categoria de outro usuário
    cat3 = Category(id=None, name="Outro", user_id=2)
    repo.create(cat3)

    # Lista todas e filtra manualmente
    user1_cats = [c for c in repo.list_all() if c.user_id == 1]
    user2_cats = [c for c in repo.list_all() if c.user_id == 2]

    assert len(user1_cats) == 2
    assert len(user2_cats) == 1
