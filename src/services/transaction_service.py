# src/services/transaction_service.py
from datetime import datetime
from typing import List
from src.models.transaction import Transaction
from src.repositories.transaction_repository import TransactionRepositoryInterface
from src.repositories.account_repository import AccountRepositoryInterface
from src.repositories.category_repository import CategoryRepositoryInterface
from src.repositories.budget_repository import BudgetRepositoryInterface


class TransactionService:
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

    def create_transaction(
        self,
        user_id: int,
        amount: float,
        type_: str,
        account_id: int,
        category_id: int,
        description: str | None = None,
    ) -> None:
        # --- Valida categoria ---
        category = self.category_repository.get_category(category_id)
        if not category:
            raise ValueError(f"Categoria não encontrada: id={category_id}")
        if category.user_id != user_id:
            raise ValueError(
                f"Categoria não pertence ao usuário. category.user_id={category.user_id}, user_id={user_id}"
            )

        # --- Valida conta ---
        account = self.account_repository.get(account_id)
        if not account:
            raise ValueError(f"Conta não encontrada: id={account_id}")
        if account.user_id != user_id:
            raise ValueError(
                f"Conta não pertence ao usuário. account.user_id={account.user_id}, user_id={user_id}"
            )

        # --- Saldo atual da conta (não somar transações antigas) ---
        current_balance = account.balance or 0.0

        # --- Calcula saldo futuro e valida ---
        new_balance = current_balance + (amount if type_ == "income" else -amount)
        if new_balance < 0:
            raise ValueError(
                f"Saldo insuficiente: saldo atual {current_balance}, gasto solicitado {amount}"
            )

        # --- Verifica limite do orçamento ---
        if type_ == "expense":
            budget = self.budget_repository.list_by_category(category_id, user_id)
            if budget:
                total_spent = sum(
                    t.amount
                    for t in self.transaction_repository.list_by_category(
                        category_id, user_id
                    )
                    if t.type == "expense"
                )
                if total_spent + amount > budget.limit_value:
                    raise ValueError(
                        f"Gasto ultrapassa orçamento: {total_spent + amount} > {budget.limit_value}"
                    )

        # --- Cria a transação ---
        transaction = Transaction(
            id=None,
            amount=amount,
            type=type_,
            account_id=account_id,
            date=datetime.now(),
            category_id=category_id,
            description=description,
            user_id=user_id,
        )
        self.transaction_repository.create(transaction)

        # --- Atualiza saldo da conta ---
        self.account_repository.update(account_id, {"balance": new_balance})

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
        transaction = self.transaction_repository.get_by_id(transaction_id)
        if not transaction or transaction.user_id != user_id:
            raise ValueError("Transação não encontrada ou pertence a outro usuário.")

        data = {}
        if amount is not None:
            data["amount"] = amount
        if type_ is not None:
            data["type"] = type_
        if category_id is not None:
            category = self.category_repository.get_category(category_id)
            if not category or category.user_id != user_id:
                raise ValueError("Categoria inválida.")
            data["category_id"] = category_id
        if description is not None:
            data["description"] = description

        self.transaction_repository.update(transaction_id, data)

    def delete_transaction(self, transaction_id: int, user_id: int) -> None:
        transaction = self.transaction_repository.get_by_id(transaction_id)
        if not transaction or transaction.user_id != user_id:
            raise ValueError("Transação não encontrada ou pertence a outro usuário.")
        self.transaction_repository.delete(transaction_id)
