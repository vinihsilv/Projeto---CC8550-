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

    def _next_transaction_id(self) -> int:
        transactions = self.transaction_repository.list_all()
        return 1 if not transactions else max(t.id for t in transactions) + 1

    def create_transaction(
        self,
        user_id: int,
        amount: float,
        type_: str,
        account_id: int,
        category_id: int,
        description: str | None = None,
    ) -> None:
        # Valida categoria pertencente ao usuário
        category = self.category_repository.get_category(category_id)
        if not category:
            raise ValueError(f"Categoria não encontrada: id={category_id}")
        if int(category.user_id) != int(user_id):
            raise ValueError(
                f"Categoria não pertence ao usuário. category.user_id={category.user_id}, user_id={user_id}"
            )

        # Valida conta (opcional, mas recomendado)
        account = self.account_repository.get(account_id)
        if not account:
            raise ValueError(f"Conta não encontrada: id={account_id}")
        if hasattr(account, "user_id") and int(getattr(account, "user_id")) != int(
            user_id
        ):
            raise ValueError(
                f"Conta não pertence ao usuário. account.user_id={getattr(account, 'user_id')}, user_id={user_id}"
            )

        transactions = self.transaction_repository.list_by_account(account_id)
        current_balance = getattr(account, "balance", 0)  # saldo inicial da conta
        current_balance += sum(
            t.amount if t.type == "income" else -t.amount for t in transactions
        )

        new_balance = current_balance + (amount if type_ == "income" else -amount)
        if new_balance < 0:
            raise ValueError(
                f"Saldo insuficiente: saldo atual {current_balance}, gasto solicitado {amount}"
            )

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

        transaction = Transaction(
            id=self._next_transaction_id(),
            account_id=account_id,
            amount=amount,
            type=type_,
            date=datetime.now(),
            category_id=category_id,
            description=description,
            user_id=user_id,
        )
        # Adiciona account_id dinamicamente no objeto
        setattr(transaction, "account_id", account_id)
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
        transaction = self.transaction_repository.get_by_id(transaction_id)
        if not transaction or transaction.user_id != user_id:
            raise ValueError("Transação não encontrada ou pertence a outro usuário.")

        data = {}
        if amount is not None:
            data["amount"] = amount
        if type_ is not None:
            data["type"] = type_
        if category_id is not None:
            category = self.category_repository.get(category_id)
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
