from src.services.transaction_service import TransactionService


class TransactionController:
    def __init__(self):
        self.service = TransactionService()

    def create_transaction(self, amount, description, category_id):
        transaction = self.service.create_transaction(amount, description, category_id)
        print(f"Transação criada: {transaction.description} - R$ {transaction.amount}")

    def list_transactions(self):
        transactions = self.service.list_transactions()
        print("\n===== Transações =====")
        if not transactions:
            print("Nenhuma transação cadastrada.")
            return
        for t in transactions:
            print(
                f"[{t.id}] R$ {t.amount} | {t.description} | Categoria: {t.category_id}"
            )

    def update_transaction(self, tid, amount, description, category_id):
        updated = self.service.update_transaction(tid, amount, description, category_id)
        if updated:
            print("Transação atualizada.")
        else:
            print("Transação não encontrada.")

    def delete_transaction(self, tid):
        deleted = self.service.delete_transaction(tid)
        if deleted:
            print("Transação removida.")
        else:
            print("Transação não encontrada.")
