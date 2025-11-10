"""
Testes do TransactionService utilizando mocks e stubs.

Este módulo testa a lógica de negócio do TransactionService isoladamente,
usando mocks para simular as dependências dos repositórios.
"""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime

from src.services.transaction_service import TransactionService
from src.models.transaction import Transaction
from src.models.account import Account
from src.models.category import Category
from src.models.budget import Budget


class TestTransactionServiceMocks:
    """Testes do TransactionService usando mocks para repositórios."""

    @pytest.fixture
    def mock_repositories(self):
        """Fixture que cria mocks para todos os repositórios."""
        return {
            "transaction_repo": Mock(),
            "account_repo": Mock(),
            "category_repo": Mock(),
            "budget_repo": Mock(),
        }

    @pytest.fixture
    def transaction_service(self, mock_repositories):
        """Fixture que cria o TransactionService com repositórios mockados."""
        return TransactionService(
            transaction_repo=mock_repositories["transaction_repo"],
            account_repo=mock_repositories["account_repo"],
            category_repo=mock_repositories["category_repo"],
            budget_repo=mock_repositories["budget_repo"],
        )

    def test_create_transaction_success(self, transaction_service, mock_repositories):
        """Testa criação de transação com sucesso usando mocks."""
        # Arrange - configurar mocks
        mock_category = Mock(spec=Category)
        mock_category.id = 1
        mock_category.user_id = 1
        mock_category.name = "Alimentação"

        mock_account = Mock(spec=Account)
        mock_account.id = 1
        mock_account.user_id = 1
        mock_account.balance = 1000.0

        mock_repositories["category_repo"].get_category.return_value = mock_category
        mock_repositories["account_repo"].get.return_value = mock_account
        mock_repositories["budget_repo"].list_by_category.return_value = None
        mock_repositories["transaction_repo"].create.return_value = None
        mock_repositories["account_repo"].update.return_value = None

        # Act
        transaction_service.create_transaction(
            user_id=1,
            amount=100.0,
            type_="expense",
            account_id=1,
            category_id=1,
            description="Compra no mercado",
        )

        # Assert - verificar se os métodos foram chamados corretamente
        mock_repositories["category_repo"].get_category.assert_called_once_with(1)
        mock_repositories["account_repo"].get.assert_called_once_with(1)
        mock_repositories["transaction_repo"].create.assert_called_once()
        mock_repositories["account_repo"].update.assert_called_once_with(
            1, {"balance": 900.0}
        )

    def test_create_transaction_category_not_found(
        self, transaction_service, mock_repositories
    ):
        """Testa erro quando categoria não é encontrada."""
        # Arrange
        mock_repositories["category_repo"].get_category.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="Categoria não encontrada: id=999"):
            transaction_service.create_transaction(
                user_id=1,
                amount=100.0,
                type_="expense",
                account_id=1,
                category_id=999,
                description="Teste",
            )

    def test_create_transaction_category_wrong_user(
        self, transaction_service, mock_repositories
    ):
        """Testa erro quando categoria pertence a outro usuário."""
        # Arrange
        mock_category = Mock(spec=Category)
        mock_category.user_id = 2  # Usuário diferente

        mock_repositories["category_repo"].get_category.return_value = mock_category

        # Act & Assert
        with pytest.raises(ValueError, match="Categoria não pertence ao usuário"):
            transaction_service.create_transaction(
                user_id=1,
                amount=100.0,
                type_="expense",
                account_id=1,
                category_id=1,
                description="Teste",
            )

    def test_create_transaction_account_not_found(
        self, transaction_service, mock_repositories
    ):
        """Testa erro quando conta não é encontrada."""
        # Arrange
        mock_category = Mock(spec=Category)
        mock_category.user_id = 1
        mock_repositories["category_repo"].get_category.return_value = mock_category
        mock_repositories["account_repo"].get.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="Conta não encontrada: id=999"):
            transaction_service.create_transaction(
                user_id=1,
                amount=100.0,
                type_="expense",
                account_id=999,
                category_id=1,
                description="Teste",
            )

    def test_create_transaction_insufficient_balance(
        self, transaction_service, mock_repositories
    ):
        """Testa erro de saldo insuficiente."""
        # Arrange
        mock_category = Mock(spec=Category)
        mock_category.user_id = 1
        mock_account = Mock(spec=Account)
        mock_account.user_id = 1
        mock_account.balance = 50.0  # Saldo menor que o gasto

        mock_repositories["category_repo"].get_category.return_value = mock_category
        mock_repositories["account_repo"].get.return_value = mock_account

        # Act & Assert
        with pytest.raises(ValueError, match="Saldo insuficiente"):
            transaction_service.create_transaction(
                user_id=1,
                amount=100.0,  # Gasto maior que o saldo
                type_="expense",
                account_id=1,
                category_id=1,
                description="Teste",
            )

    def test_create_transaction_budget_exceeded(
        self, transaction_service, mock_repositories
    ):
        """Testa erro quando orçamento é excedido."""
        # Arrange
        mock_category = Mock(spec=Category)
        mock_category.user_id = 1

        mock_account = Mock(spec=Account)
        mock_account.user_id = 1
        mock_account.balance = 1000.0

        mock_budget = Mock(spec=Budget)
        mock_budget.limit_value = 200.0

        # Simular transações existentes totalizando 150
        existing_transactions = [
            Mock(amount=100.0, type="expense"),
            Mock(amount=50.0, type="expense"),
        ]

        mock_repositories["category_repo"].get_category.return_value = mock_category
        mock_repositories["account_repo"].get.return_value = mock_account
        mock_repositories["budget_repo"].list_by_category.return_value = mock_budget
        mock_repositories["transaction_repo"].list_by_category.return_value = (
            existing_transactions
        )

        # Act & Assert - Tentar gastar 100 quando já gastou 150, limite 200
        with pytest.raises(ValueError, match="Gasto ultrapassa orçamento"):
            transaction_service.create_transaction(
                user_id=1,
                amount=100.0,  # 150 + 100 = 250 > 200
                type_="expense",
                account_id=1,
                category_id=1,
                description="Teste orçamento",
            )

    def test_create_income_transaction(self, transaction_service, mock_repositories):
        """Testa criação de transação de receita."""
        # Arrange
        mock_category = Mock(spec=Category)
        mock_category.user_id = 1
        mock_account = Mock(spec=Account)
        mock_account.user_id = 1
        mock_account.balance = 500.0

        mock_repositories["category_repo"].get_category.return_value = mock_category
        mock_repositories["account_repo"].get.return_value = mock_account
        mock_repositories["budget_repo"].list_by_category.return_value = None

        # Act
        transaction_service.create_transaction(
            user_id=1,
            amount=200.0,
            type_="income",
            account_id=1,
            category_id=1,
            description="Salário",
        )

        # Assert - Saldo deve aumentar para 700.0
        mock_repositories["account_repo"].update.assert_called_once_with(
            1, {"balance": 700.0}
        )

    def test_get_transaction_success(self, transaction_service, mock_repositories):
        """Testa busca de transação com sucesso."""
        # Arrange
        mock_transaction = Mock(spec=Transaction)
        mock_transaction.id = 1
        mock_transaction.amount = 100.0
        mock_repositories["transaction_repo"].get_by_id.return_value = mock_transaction

        # Act
        result = transaction_service.get_transaction(1)

        # Assert
        assert result == mock_transaction
        mock_repositories["transaction_repo"].get_by_id.assert_called_once_with(1)

    def test_get_transaction_not_found(self, transaction_service, mock_repositories):
        """Testa erro quando transação não é encontrada."""
        # Arrange
        mock_repositories["transaction_repo"].get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="Transaction not found"):
            transaction_service.get_transaction(999)

    def test_list_transactions(self, transaction_service, mock_repositories):
        """Testa listagem de transações por usuário."""
        # Arrange
        mock_transactions = [Mock(spec=Transaction), Mock(spec=Transaction)]
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            mock_transactions
        )

        # Act
        result = transaction_service.list_transactions(1)

        # Assert
        assert result == mock_transactions
        mock_repositories["transaction_repo"].list_by_user.assert_called_once_with(1)

    def test_update_transaction_success(self, transaction_service, mock_repositories):
        """Testa atualização de transação com sucesso."""
        # Arrange
        mock_transaction = Mock(spec=Transaction)
        mock_transaction.user_id = 1
        mock_category = Mock(spec=Category)
        mock_category.user_id = 1

        mock_repositories["transaction_repo"].get_by_id.return_value = mock_transaction
        mock_repositories["category_repo"].get_category.return_value = mock_category

        # Act
        transaction_service.update_transaction(
            transaction_id=1,
            user_id=1,
            amount=150.0,
            category_id=2,
            description="Atualizada",
        )

        # Assert
        expected_data = {"amount": 150.0, "category_id": 2, "description": "Atualizada"}
        mock_repositories["transaction_repo"].update.assert_called_once_with(
            1, expected_data
        )

    def test_update_transaction_not_found(self, transaction_service, mock_repositories):
        """Testa erro ao atualizar transação inexistente."""
        # Arrange
        mock_repositories["transaction_repo"].get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(
            ValueError, match="Transação não encontrada ou pertence a outro usuário"
        ):
            transaction_service.update_transaction(1, 1, amount=100.0)

    def test_delete_transaction_success(self, transaction_service, mock_repositories):
        """Testa exclusão de transação com sucesso."""
        # Arrange
        mock_transaction = Mock(spec=Transaction)
        mock_transaction.user_id = 1
        mock_repositories["transaction_repo"].get_by_id.return_value = mock_transaction

        # Act
        transaction_service.delete_transaction(1, 1)

        # Assert
        mock_repositories["transaction_repo"].delete.assert_called_once_with(1)

    def test_delete_transaction_wrong_user(
        self, transaction_service, mock_repositories
    ):
        """Testa erro ao deletar transação de outro usuário."""
        # Arrange
        mock_transaction = Mock(spec=Transaction)
        mock_transaction.user_id = 2  # Usuário diferente
        mock_repositories["transaction_repo"].get_by_id.return_value = mock_transaction

        # Act & Assert
        with pytest.raises(
            ValueError, match="Transação não encontrada ou pertence a outro usuário"
        ):
            transaction_service.delete_transaction(1, 1)
