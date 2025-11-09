from sqlalchemy.orm import Session
from src.models.category import Category
from src.interfaces.category_repository_interface import CategoryRepositoryInterface


class CategoryRepository(CategoryRepositoryInterface):
    """SQLAlchemy implementation of CategoryRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, category: Category) -> Category:
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def list_all(self) -> list[Category]:
        return self.session.query(Category).all()

    def get_category(self, category_id: int) -> Category | None:
        return self.session.query(Category).filter_by(id=category_id).first()

    def update(self, category_id: int, name: str) -> Category | None:
        category = self.get_category(category_id)
        if category:
            category.name = name
            self.session.commit()
            self.session.refresh(category)
            return category
        return None

    def delete(self, category_id: int) -> bool:
        category = self.get_category(category_id)
        if category:
            self.session.delete(category)
            self.session.commit()
            return True
        return False

    # Mantido para compatibilidade
    def get(self, category_id: int) -> Category | None:
        return self.get_category(category_id)
