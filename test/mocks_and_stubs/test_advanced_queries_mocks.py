"""
Testes das funções de consulta com ordenação e filtro do TransactionService.

Este módulo testa as novas funcionalidades de busca avançada e resumo
de transações usando mocks para isolar as dependências.
"""

import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta

from src.services.transaction_service import TransactionService
from src.models.transaction import Transaction
from src.models.account import Account
from src.models.category import Category


class TestTransactionServiceAdvancedQueries:
    """Testes para consultas avançadas do TransactionService."""

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

    @pytest.fixture
    def sample_transactions(self):
        """Fixture que cria transações de exemplo para testes."""
        base_date = datetime(2024, 1, 1)

        transactions = [
            Mock(
                id=1,
                user_id=1,
                amount=100.0,
                type="expense",
                date=base_date,
                category_id=1,
                account_id=1,
                description="Compra no mercado",
            ),
            Mock(
                id=2,
                user_id=1,
                amount=500.0,
                type="income",
                date=base_date + timedelta(days=1),
                category_id=2,
                account_id=1,
                description="Salário",
            ),
            Mock(
                id=3,
                user_id=1,
                amount=50.0,
                type="expense",
                date=base_date + timedelta(days=2),
                category_id=1,
                account_id=2,
                description="Lanche",
            ),
            Mock(
                id=4,
                user_id=1,
                amount=200.0,
                type="expense",
                date=base_date + timedelta(days=3),
                category_id=3,
                account_id=1,
                description="Combustível",
            ),
            Mock(
                id=5,
                user_id=1,
                amount=1000.0,
                type="income",
                date=datetime(2024, 2, 1),
                category_id=2,
                account_id=1,
                description="Freelance",
            ),
        ]

        return transactions

    # ===== TESTES PARA search_transactions_with_filters =====

    def test_search_transactions_no_filters(
        self, transaction_service, mock_repositories, sample_transactions
    ):
        """Testa busca sem filtros (deve retornar todas as transações ordenadas por data desc)."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            sample_transactions
        )

        # Act
        result = transaction_service.search_transactions_with_filters(user_id=1)

        # Assert
        assert len(result) == 5
        # Verificar ordenação por data (desc - mais recente primeiro)
        assert result[0].date > result[1].date

    def test_search_transactions_filter_by_type(
        self, transaction_service, mock_repositories, sample_transactions
    ):
        """Testa filtro por tipo de transação."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            sample_transactions
        )

        # Act - filtrar apenas despesas
        expenses = transaction_service.search_transactions_with_filters(
            user_id=1, transaction_type="expense"
        )

        # Act - filtrar apenas receitas
        incomes = transaction_service.search_transactions_with_filters(
            user_id=1, transaction_type="income"
        )

        # Assert
        assert len(expenses) == 3
        assert all(t.type == "expense" for t in expenses)
        assert len(incomes) == 2
        assert all(t.type == "income" for t in incomes)

    def test_search_transactions_filter_by_amount_range(
        self, transaction_service, mock_repositories, sample_transactions
    ):
        """Testa filtro por faixa de valores."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            sample_transactions
        )

        # Act
        result = transaction_service.search_transactions_with_filters(
            user_id=1, min_amount=100.0, max_amount=500.0
        )

        # Assert
        assert len(result) == 3  # 100, 200, 500
        assert all(100.0 <= t.amount <= 500.0 for t in result)

    def test_search_transactions_filter_by_date_range(
        self, transaction_service, mock_repositories, sample_transactions
    ):
        """Testa filtro por período de datas."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            sample_transactions
        )
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 3)

        # Act
        result = transaction_service.search_transactions_with_filters(
            user_id=1, start_date=start_date, end_date=end_date
        )

        # Assert
        assert len(result) == 3  # Primeiras 3 transações
        assert all(start_date <= t.date <= end_date for t in result)

    def test_search_transactions_filter_by_category(
        self, transaction_service, mock_repositories, sample_transactions
    ):
        """Testa filtro por categoria."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            sample_transactions
        )

        # Act
        result = transaction_service.search_transactions_with_filters(
            user_id=1, category_id=1
        )

        # Assert
        assert len(result) == 2  # Transações da categoria 1
        assert all(t.category_id == 1 for t in result)

    def test_search_transactions_filter_by_description(
        self, transaction_service, mock_repositories, sample_transactions
    ):
        """Testa filtro por texto na descrição."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            sample_transactions
        )

        # Act
        result = transaction_service.search_transactions_with_filters(
            user_id=1, description_contains="Salário"
        )

        # Assert
        assert len(result) == 1
        assert "Salário" in result[0].description

    def test_search_transactions_sort_by_amount(
        self, transaction_service, mock_repositories, sample_transactions
    ):
        """Testa ordenação por valor."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            sample_transactions
        )

        # Act - ordenar por valor crescente
        result_asc = transaction_service.search_transactions_with_filters(
            user_id=1, sort_by="amount", sort_order="asc"
        )

        # Act - ordenar por valor decrescente
        result_desc = transaction_service.search_transactions_with_filters(
            user_id=1, sort_by="amount", sort_order="desc"
        )

        # Assert
        assert result_asc[0].amount == 50.0  # Menor valor
        assert result_asc[-1].amount == 1000.0  # Maior valor
        assert result_desc[0].amount == 1000.0  # Maior valor
        assert result_desc[-1].amount == 50.0  # Menor valor

    def test_search_transactions_invalid_sort_field(
        self, transaction_service, mock_repositories
    ):
        """Testa erro com campo de ordenação inválido."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = []

        # Act & Assert
        with pytest.raises(ValueError, match="Campo de ordenação inválido"):
            transaction_service.search_transactions_with_filters(
                user_id=1, sort_by="invalid_field"
            )

    def test_search_transactions_invalid_amount_range(
        self, transaction_service, mock_repositories
    ):
        """Testa erro com faixa de valores inválida."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = []

        # Act & Assert
        with pytest.raises(
            ValueError, match="Valor mínimo não pode ser maior que o valor máximo"
        ):
            transaction_service.search_transactions_with_filters(
                user_id=1, min_amount=100.0, max_amount=50.0
            )

    # ===== TESTES PARA get_transactions_summary =====

    def test_summary_group_by_category(
        self, transaction_service, mock_repositories, sample_transactions
    ):
        """Testa resumo agrupado por categoria."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            sample_transactions
        )

        # Mock das categorias
        mock_cat1 = Mock()
        mock_cat1.name = "Alimentação"
        mock_cat2 = Mock()
        mock_cat2.name = "Salário"
        mock_cat3 = Mock()
        mock_cat3.name = "Transporte"

        mock_categories = {1: mock_cat1, 2: mock_cat2, 3: mock_cat3}
        mock_repositories["category_repo"].get_category.side_effect = (
            lambda cid: mock_categories.get(cid)
        )

        # Act
        result = transaction_service.get_transactions_summary(
            user_id=1, group_by="category"
        )

        # Assert
        assert len(result) == 3  # 3 categorias diferentes

        # Verificar categoria 1 (Alimentação): 100 + 50 = 150
        alimentacao = next((r for r in result if r["group_key"] == 1), None)
        assert alimentacao is not None
        assert alimentacao["group_name"] == "Alimentação"
        assert alimentacao["total_amount"] == 150.0
        assert alimentacao["count"] == 2
        assert alimentacao["avg_amount"] == 75.0

    def test_summary_group_by_account(
        self, transaction_service, mock_repositories, sample_transactions
    ):
        """Testa resumo agrupado por conta."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            sample_transactions
        )

        # Mock das contas
        mock_acc1 = Mock()
        mock_acc1.name = "Conta Corrente"
        mock_acc2 = Mock()
        mock_acc2.name = "Poupança"

        mock_accounts = {1: mock_acc1, 2: mock_acc2}
        mock_repositories["account_repo"].get.side_effect = (
            lambda aid: mock_accounts.get(aid)
        )

        # Act
        result = transaction_service.get_transactions_summary(
            user_id=1, group_by="account"
        )

        # Assert
        assert len(result) == 2  # 2 contas diferentes

    def test_summary_group_by_type(
        self, transaction_service, mock_repositories, sample_transactions
    ):
        """Testa resumo agrupado por tipo."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            sample_transactions
        )

        # Act
        result = transaction_service.get_transactions_summary(
            user_id=1, group_by="type"
        )

        # Assert
        assert len(result) == 2  # income e expense

        # Verificar totais
        expense_summary = next((r for r in result if r["group_key"] == "expense"), None)
        income_summary = next((r for r in result if r["group_key"] == "income"), None)

        assert expense_summary["total_amount"] == 350.0  # 100 + 50 + 200
        assert expense_summary["count"] == 3
        assert income_summary["total_amount"] == 1500.0  # 500 + 1000
        assert income_summary["count"] == 2

    def test_summary_group_by_month(
        self, transaction_service, mock_repositories, sample_transactions
    ):
        """Testa resumo agrupado por mês."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            sample_transactions
        )

        # Act
        result = transaction_service.get_transactions_summary(
            user_id=1, group_by="month"
        )

        # Assert
        assert len(result) == 2  # Janeiro (4 transações) e Fevereiro (1 transação)

    def test_summary_with_period_filter(
        self, transaction_service, mock_repositories, sample_transactions
    ):
        """Testa resumo com filtro de período."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            sample_transactions
        )
        mock_repositories["category_repo"].get_category.return_value = Mock(
            name="Teste"
        )

        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 3)

        # Act
        result = transaction_service.get_transactions_summary(
            user_id=1, group_by="category", period_start=start_date, period_end=end_date
        )

        # Assert - deve considerar apenas as 3 primeiras transações
        total_transactions = sum(r["count"] for r in result)
        assert total_transactions == 3

    def test_summary_sort_by_count(
        self, transaction_service, mock_repositories, sample_transactions
    ):
        """Testa ordenação do resumo por quantidade de transações."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = (
            sample_transactions
        )
        mock_repositories["category_repo"].get_category.return_value = Mock(
            name="Teste"
        )

        # Act
        result = transaction_service.get_transactions_summary(
            user_id=1, group_by="category", sort_by="count", sort_order="desc"
        )

        # Assert - categoria 1 tem 2 transações, deve vir primeiro
        assert result[0]["count"] >= result[1]["count"]

    def test_summary_invalid_group_by(self, transaction_service, mock_repositories):
        """Testa erro com agrupamento inválido."""
        # Arrange
        mock_repositories["transaction_repo"].list_by_user.return_value = []

        # Act & Assert
        with pytest.raises(ValueError, match="Agrupamento inválido"):
            transaction_service.get_transactions_summary(user_id=1, group_by="invalid")
