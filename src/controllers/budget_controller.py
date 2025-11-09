from src.services.budget_service import BudgetService


class BudgetController:
    def __init__(self):
        self.service = BudgetService()

    def create_budget(self, category_id, year, month, limit_value):
        self.service.create_budget(category_id, year, month, limit_value)
        print("Orçamento criado com sucesso.")

    def list_budgets(self):
        budgets = self.service.list_budgets()
        if not budgets:
            print("Nenhum orçamento encontrado.")
        else:
            for b in budgets:
                print(
                    f"{b.id} | Categoria: {b.category_id} | {b.month}/{b.year} | Limite: {b.limit_value}"
                )

    def update_budget(
        self, budget_id, category_id=None, year=None, month=None, limit_value=None
    ):
        self.service.update_budget(
            budget_id,
            category_id=category_id,
            year=year,
            month=month,
            limit_value=limit_value,
        )
        print("Orçamento atualizado com sucesso.")

    def delete_budget(self, budget_id):
        self.service.delete_budget(budget_id)
        print("Orçamento removido.")
