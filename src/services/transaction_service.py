from datetime import datetime
from typing import List
from src.models.transaction import Transaction
from src.repositories.transaction_repository import TransactionRepositoryInterface
from src.repositories.account_repository import AccountRepositoryInterface
from src.repositories.category_repository import CategoryRepositoryInterface
from src.repositories.budget_repository import BudgetRepositoryInterface


class TransactionService:
    """Handles business rules for transactions, including validations and reports."""

    def __init__(
        self,
        transaction_repo: TransactionRepositoryInterface,
        account_repo: AccountRepositoryInterface,
        category_repo: CategoryRepositoryInterface,
        budget_repo: BudgetRepositoryInterface,
    ):
        self.transaction_repository = transaction_repo
        self.account_repository = account_repo
        self.category_repository = category_repo
        self.budget_repository = budget_repo

    def _next_transaction_id(self) -> int:
        transactions = self.transaction_repository.list_all()
        return 1 if not transactions else max(t.id for t in transactions) + 1

    def create_transaction(
        self,
        user_id: int,
        amount: float,
        type_: str,  # "income" ou "expense"
        account_id: int,
        category_id: int,
        description: str | None = None,
    ) -> None:
        # Valida categoria
        category = self.category_repository.get(category_id)
        if not category or category.user_id != user_id:
            raise ValueError("Categoria inválida ou não pertence ao usuário.")

        # Calcula saldo atual da conta
        account = self.account_repository.get(account_id)
        transactions = self.transaction_repository.list_by_account(account_id)
        current_balance = sum(
            t.amount if t.type == "income" else -t.amount for t in transactions
        )
        new_balance = current_balance + (amount if type_ == "income" else -amount)
        if new_balance < 0:
            raise ValueError(
                f"Saldo insuficiente: saldo atual {current_balance}, gasto solicitado {amount}"
            )

        # Verifica orçamento da categoria
        if type_ == "expense":
            budget = self.budget_repository.find_by_category(category_id, user_id)
            if budget:
                total_spent = sum(
                    t.amount
                    for t in self.transaction_repository.list_by_category(
                        category_id, user_id
                    )
                    if t.type == "expense"
                )
                projected_total = total_spent + amount
                if projected_total > budget.limit_value:
                    raise ValueError(
                        f"Gasto ultrapassa orçamento: {projected_total} > {budget.limit_value}"
                    )

        # Cria a transação
        transaction = Transaction(
            id=self._next_transaction_id(),
            amount=amount,
            type=type_,
            date=datetime.now(),
            category_id=category_id,
            description=description,
            user_id=user_id,
        )
        self.transaction_repository.create(transaction)

    def list_transactions(self, user_id: int) -> List[Transaction]:
        return self.transaction_repository.list_by_user(user_id)

    def update_transaction(
        self,
        transaction_id: int,
        user_id: int,
        amount: float | None = None,
        type_: str | None = None,
        category_id: int | None = None,
        description: str | None = None,
    ) -> None:
        transaction = self.transaction_repository.get(transaction_id)
        if not transaction or transaction.user_id != user_id:
            raise ValueError("Transação não encontrada ou pertence a outro usuário.")

        data = {}
        if amount is not None:
            data["amount"] = amount
        if type_ is not None:
            data["type"] = type_
        if category_id is not None:
            # Valida categoria
            category = self.category_repository.get(category_id)
            if not category or category.user_id != user_id:
                raise ValueError("Categoria inválida.")
            data["category_id"] = category_id
        if description is not None:
            data["description"] = description

        self.transaction_repository.update(transaction_id, data)

    def delete_transaction(self, transaction_id: int, user_id: int) -> None:
        transaction = self.transaction_repository.get(transaction_id)
        if not transaction or transaction.user_id != user_id:
            raise ValueError("Transação não encontrada ou pertence a outro usuário.")
        self.transaction_repository.delete(transaction_id)

    def generate_monthly_report(self, user_id: int, year: int, month: int) -> dict:
        transactions = self.transaction_repository.list_by_user_and_month(
            user_id, year, month
        )
        total_income = sum(t.amount for t in transactions if t.type == "income")
        total_expense = sum(t.amount for t in transactions if t.type == "expense")

        expenses_by_category = {}
        for t in transactions:
            if t.type == "expense":
                expenses_by_category[t.category_id] = (
                    expenses_by_category.get(t.category_id, 0) + t.amount
                )

        report = {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": total_income - total_expense,
            "expenses_by_category": expenses_by_category,
        }
        return report
