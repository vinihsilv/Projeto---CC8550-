from src.services.category_service import CategoryService


class CategoryController:
    def __init__(self):
        self.service = CategoryService()

    def create_category(self, name, description=None):
        category = self.service.create_category(name, description)
        print(f"Categoria criada: {category}")

    def list_categories(self):
        categories = self.service.list_categories()
        if not categories:
            print("Nenhuma categoria cadastrada.")
            return

        for c in categories:
            print(f"[{c.id}] {c.name} - {c.description}")

    def update_category(self, category_id, name, description=None):
        updated = self.service.update_category(category_id, name, description)
        if updated:
            print("Categoria atualizada:", updated)
        else:
            print("Categoria não encontrada.")

    def delete_category(self, category_id):
        deleted = self.service.delete_category(category_id)
        if deleted:
            print("Categoria deletada.")
        else:
            print("Categoria não encontrada.")
