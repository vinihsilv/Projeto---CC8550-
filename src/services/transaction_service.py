# src/services/transaction_service.py
from datetime import datetime
from typing import List, Dict, Any
from src.models.transaction import Transaction
from src.repositories.transaction_repository import TransactionRepositoryInterface
from src.repositories.account_repository import AccountRepositoryInterface
from src.repositories.category_repository import CategoryRepositoryInterface
from src.repositories.budget_repository import BudgetRepositoryInterface
from src.services.exceptions import (
    CategoryNotFoundError,
    CategoryOwnershipError,
    AccountNotFoundError,
    AccountOwnershipError,
    InsufficientBalanceError,
    BudgetExceededError,
    TransactionNotFoundError,
)


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
            raise CategoryNotFoundError(f"Categoria não encontrada: id={category_id}")
        if category.user_id != user_id:
            raise CategoryOwnershipError(
                f"Categoria não pertence ao usuário. category.user_id={category.user_id}, user_id={user_id}"
            )

        # --- Valida conta ---
        account = self.account_repository.get(account_id)
        if not account:
            raise AccountNotFoundError(f"Conta não encontrada: id={account_id}")
        if account.user_id != user_id:
            raise AccountOwnershipError(
                f"Conta não pertence ao usuário. account.user_id={account.user_id}, user_id={user_id}"
            )

        # --- Saldo atual da conta (não somar transações antigas) ---
        current_balance = account.balance or 0.0

        # --- Calcula saldo futuro e valida ---
        new_balance = current_balance + (amount if type_ == "income" else -amount)
        if new_balance < 0:
            raise InsufficientBalanceError(
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
                    raise BudgetExceededError(
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

    # no TransactionService

    def get_transaction(self, transaction_id: int) -> Transaction:
        transaction = self.transaction_repository.get_by_id(transaction_id)
        if not transaction:
            raise TransactionNotFoundError("Transaction not found")
        return transaction

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
            raise TransactionNotFoundError(
                "Transação não encontrada ou pertence a outro usuário."
            )

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
            raise TransactionNotFoundError(
                "Transação não encontrada ou pertence a outro usuário."
            )
        self.transaction_repository.delete(transaction_id)

    def search_transactions_with_filters(
        self,
        user_id: int,
        transaction_type: str | None = None,
        min_amount: float | None = None,
        max_amount: float | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        category_id: int | None = None,
        account_id: int | None = None,
        description_contains: str | None = None,
        sort_by: str = "date",
        sort_order: str = "desc",
    ) -> List[Transaction]:
        """
        Busca transações com filtros avançados e ordenação.

        Args:
            user_id: ID do usuário
            transaction_type: Tipo da transação ("income" ou "expense")
            min_amount: Valor mínimo
            max_amount: Valor máximo
            start_date: Data de início
            end_date: Data final
            category_id: ID da categoria
            account_id: ID da conta
            description_contains: Texto contido na descrição
            sort_by: Campo para ordenação ("date", "amount", "description")
            sort_order: Ordem ("asc" ou "desc")

        Returns:
            Lista de transações filtradas e ordenadas
        """
        # Validações de entrada
        if sort_by not in ["date", "amount", "description", "type"]:
            raise ValueError(
                "Campo de ordenação inválido. Use: date, amount, description, type"
            )

        if sort_order not in ["asc", "desc"]:
            raise ValueError("Ordem de classificação inválida. Use: asc ou desc")

        if min_amount is not None and min_amount < 0:
            raise ValueError("Valor mínimo deve ser positivo")

        if max_amount is not None and max_amount < 0:
            raise ValueError("Valor máximo deve ser positivo")

        if (
            min_amount is not None
            and max_amount is not None
            and min_amount > max_amount
        ):
            raise ValueError("Valor mínimo não pode ser maior que o valor máximo")

        if start_date is not None and end_date is not None and start_date > end_date:
            raise ValueError("Data de início não pode ser posterior à data final")

        # Buscar todas as transações do usuário
        all_transactions = self.transaction_repository.list_by_user(user_id)

        # Aplicar filtros
        filtered_transactions = []
        for transaction in all_transactions:
            # Filtro por tipo
            if transaction_type and transaction.type != transaction_type:
                continue

            # Filtro por valor mínimo
            if min_amount is not None and transaction.amount < min_amount:
                continue

            # Filtro por valor máximo
            if max_amount is not None and transaction.amount > max_amount:
                continue

            # Filtro por data de início
            if start_date and transaction.date < start_date:
                continue

            # Filtro por data final
            if end_date and transaction.date > end_date:
                continue

            # Filtro por categoria
            if category_id and transaction.category_id != category_id:
                continue

            # Filtro por conta
            if account_id and transaction.account_id != account_id:
                continue

            # Filtro por descrição
            if description_contains and (
                not transaction.description
                or description_contains.lower() not in transaction.description.lower()
            ):
                continue

            filtered_transactions.append(transaction)

        # Aplicar ordenação
        reverse_order = sort_order == "desc"

        if sort_by == "date":
            filtered_transactions.sort(key=lambda t: t.date, reverse=reverse_order)
        elif sort_by == "amount":
            filtered_transactions.sort(key=lambda t: t.amount, reverse=reverse_order)
        elif sort_by == "description":
            filtered_transactions.sort(
                key=lambda t: t.description or "", reverse=reverse_order
            )
        elif sort_by == "type":
            filtered_transactions.sort(key=lambda t: t.type, reverse=reverse_order)

        return filtered_transactions

    def get_transactions_summary(
        self,
        user_id: int,
        group_by: str = "category",
        period_start: datetime | None = None,
        period_end: datetime | None = None,
        transaction_type: str | None = None,
        sort_by: str = "total_amount",
        sort_order: str = "desc",
    ) -> List[dict]:
        """
        Obtém resumo de transações agrupadas com totalizadores.

        Args:
            user_id: ID do usuário
            group_by: Agrupamento ("category", "account", "type", "month")
            period_start: Data de início do período
            period_end: Data final do período
            transaction_type: Filtro por tipo ("income" ou "expense")
            sort_by: Campo para ordenação ("total_amount", "count", "avg_amount")
            sort_order: Ordem ("asc" ou "desc")

        Returns:
            Lista de dicionários com resumo agrupado
        """
        # Validações
        if group_by not in ["category", "account", "type", "month"]:
            raise ValueError(
                "Agrupamento inválido. Use: category, account, type, month"
            )

        if sort_by not in ["total_amount", "count", "avg_amount"]:
            raise ValueError(
                "Campo de ordenação inválido. Use: total_amount, count, avg_amount"
            )

        if sort_order not in ["asc", "desc"]:
            raise ValueError("Ordem inválida. Use: asc ou desc")

        # Buscar transações do período
        transactions = self.transaction_repository.list_by_user(user_id)

        # Filtrar por período e tipo
        filtered_transactions = []
        for transaction in transactions:
            # Filtro por período
            if period_start and transaction.date < period_start:
                continue
            if period_end and transaction.date > period_end:
                continue

            # Filtro por tipo
            if transaction_type and transaction.type != transaction_type:
                continue

            filtered_transactions.append(transaction)

        # Agrupar transações
        groups = {}

        for transaction in filtered_transactions:
            # Determinar chave do grupo
            if group_by == "category":
                key = transaction.category_id
                # Buscar nome da categoria
                category = self.category_repository.get_category(
                    transaction.category_id
                )
                name = (
                    category.name
                    if category
                    else f"Categoria {transaction.category_id}"
                )
            elif group_by == "account":
                key = transaction.account_id
                # Buscar nome da conta
                account = self.account_repository.get(transaction.account_id)
                name = account.name if account else f"Conta {transaction.account_id}"
            elif group_by == "type":
                key = transaction.type
                name = "Receita" if transaction.type == "income" else "Despesa"
            elif group_by == "month":
                key = f"{transaction.date.year}-{transaction.date.month:02d}"
                name = f"{transaction.date.strftime('%B')} {transaction.date.year}"

            # Inicializar grupo se necessário
            if key not in groups:
                groups[key] = {
                    "group_key": key,
                    "group_name": name,
                    "transactions": [],
                    "total_amount": 0.0,
                    "count": 0,
                }

            # Adicionar transação ao grupo
            groups[key]["transactions"].append(transaction)
            groups[key]["total_amount"] += transaction.amount
            groups[key]["count"] += 1

        # Calcular médias e preparar resultado
        result = []
        for group_data in groups.values():
            summary = {
                "group_key": group_data["group_key"],
                "group_name": group_data["group_name"],
                "total_amount": round(group_data["total_amount"], 2),
                "count": group_data["count"],
                "avg_amount": (
                    round(group_data["total_amount"] / group_data["count"], 2)
                    if group_data["count"] > 0
                    else 0.0
                ),
            }
            result.append(summary)

        # Ordenar resultado
        reverse_order = sort_order == "desc"

        if sort_by == "total_amount":
            result.sort(key=lambda x: x["total_amount"], reverse=reverse_order)
        elif sort_by == "count":
            result.sort(key=lambda x: x["count"], reverse=reverse_order)
        elif sort_by == "avg_amount":
            result.sort(key=lambda x: x["avg_amount"], reverse=reverse_order)

        return result
