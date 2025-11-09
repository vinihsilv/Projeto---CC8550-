from src.services.category_service import CategoryService


class CategoryController:
    def __init__(self):
        self.service = CategoryService()

    def create_category(self, name):
        category = self.service.create_category(name)
        print(f"Categoria criada: {category.name} (ID: {category.id})")

    def list_categories(self):
        categories = self.service.list_categories()
        print("\n===== Categorias =====")
        if not categories:
            print("Nenhuma categoria cadastrada.")
            return
        for c in categories:
            print(f"[{c.id}] {c.name}")

    def update_category(self, category_id, new_name):
        updated = self.service.update_category(category_id, new_name)
        if updated:
            print("Categoria atualizada.")
        else:
            print("Categoria não encontrada.")

    def delete_category(self, category_id):
        deleted = self.service.delete_category(category_id)
        if deleted:
            print("Categoria removida.")
        else:
            print("Categoria não encontrada.")
