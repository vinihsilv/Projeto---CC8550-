"""
Testes do BudgetService combinando mocks e stubs.

Este módulo demonstra o uso combinado de mocks e stubs para testar
diferentes aspectos da lógica de negócio do BudgetService.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from typing import List

from src.services.budget_service import BudgetService
from src.models.budget import Budget


class BudgetRepositoryStub:
    """Stub específico para BudgetRepository com comportamentos personalizados."""

    def __init__(self):
        self.budgets = {}
        self.next_id = 1
        self.should_raise_exception = False
        self.exception_method = None

    def create(self, budget: Budget) -> Budget:
        if self.should_raise_exception and self.exception_method == "create":
            raise RuntimeError("Erro de conexão com banco de dados")

        budget.id = self.next_id
        self.budgets[self.next_id] = budget
        self.next_id += 1
        return budget

    def list_by_user(self, user_id: int) -> List[Budget]:
        if self.should_raise_exception and self.exception_method == "list":
            raise RuntimeError("Erro de conexão com banco de dados")

        return [b for b in self.budgets.values() if b.user_id == user_id]

    def get(self, budget_id: int) -> Budget | None:
        if self.should_raise_exception and self.exception_method == "get":
            raise RuntimeError("Erro de conexão com banco de dados")

        return self.budgets.get(budget_id)

    def update(self, budget_id: int, data: dict) -> Budget | None:
        if self.should_raise_exception and self.exception_method == "update":
            raise RuntimeError("Erro de conexão com banco de dados")

        budget = self.budgets.get(budget_id)
        if budget:
            for key, value in data.items():
                setattr(budget, key, value)
        return budget

    def delete(self, budget_id: int) -> bool:
        if self.should_raise_exception and self.exception_method == "delete":
            raise RuntimeError("Erro de conexão com banco de dados")

        if budget_id in self.budgets:
            del self.budgets[budget_id]
            return True
        return False

    def simulate_error(self, method_name: str):
        """Configura o stub para simular erro em método específico."""
        self.should_raise_exception = True
        self.exception_method = method_name

    def clear_error(self):
        """Remove simulação de erro."""
        self.should_raise_exception = False
        self.exception_method = None


class TestBudgetServiceMocksAndStubs:
    """Testes combinando mocks e stubs."""

    @pytest.fixture
    def budget_repository_stub(self):
        """Fixture que fornece um stub do repositório."""
        return BudgetRepositoryStub()

    @pytest.fixture
    def budget_service_with_stub(self, budget_repository_stub):
        """Fixture que cria o service com repositório stub."""
        return BudgetService(repository=budget_repository_stub)

    @pytest.fixture
    def mock_repository(self):
        """Fixture que fornece um mock do repositório."""
        return Mock()

    @pytest.fixture
    def budget_service_with_mock(self, mock_repository):
        """Fixture que cria o service com repositório mock."""
        return BudgetService(repository=mock_repository)

    # ===== TESTES COM STUBS =====

    def test_create_budget_success_stub(
        self, budget_service_with_stub, budget_repository_stub
    ):
        """Testa criação de orçamento com stub - cenário de sucesso."""
        # Act
        budget = budget_service_with_stub.create_budget(
            user_id=1, category_id=1, year=2024, month=1, limit_value=1000.0
        )

        # Assert
        assert budget.id == 1
        assert budget.user_id == 1
        assert budget.category_id == 1
        assert budget.year == 2024
        assert budget.month == 1
        assert budget.limit_value == 1000.0
        assert len(budget_repository_stub.budgets) == 1

    def test_create_budget_invalid_month_stub(self, budget_service_with_stub):
        """Testa validação de mês inválido com stub."""
        # Act & Assert
        with pytest.raises(ValueError, match="Mês inválido \\(1-12\\)"):
            budget_service_with_stub.create_budget(
                user_id=1, category_id=1, year=2024, month=13, limit_value=1000.0
            )

        with pytest.raises(ValueError, match="Mês inválido \\(1-12\\)"):
            budget_service_with_stub.create_budget(
                user_id=1, category_id=1, year=2024, month=0, limit_value=1000.0
            )

    def test_create_budget_invalid_limit_stub(self, budget_service_with_stub):
        """Testa validação de limite inválido com stub."""
        # Act & Assert
        with pytest.raises(ValueError, match="Limite deve ser positivo"):
            budget_service_with_stub.create_budget(
                user_id=1, category_id=1, year=2024, month=1, limit_value=0
            )

        with pytest.raises(ValueError, match="Limite deve ser positivo"):
            budget_service_with_stub.create_budget(
                user_id=1, category_id=1, year=2024, month=1, limit_value=-100
            )

    def test_create_budget_duplicate_stub(self, budget_service_with_stub):
        """Testa criação de orçamento duplicado com stub."""
        # Arrange - criar primeiro orçamento
        budget_service_with_stub.create_budget(
            user_id=1, category_id=1, year=2024, month=1, limit_value=1000.0
        )

        # Act & Assert - tentar criar duplicado
        with pytest.raises(
            ValueError, match="Já existe orçamento para este usuário neste mês"
        ):
            budget_service_with_stub.create_budget(
                user_id=1, category_id=2, year=2024, month=1, limit_value=500.0
            )

    def test_list_budgets_multiple_users_stub(self, budget_service_with_stub):
        """Testa listagem de orçamentos com múltiplos usuários usando stub."""
        # Arrange - criar orçamentos para diferentes usuários
        budget_service_with_stub.create_budget(1, 1, 2024, 1, 1000.0)
        budget_service_with_stub.create_budget(1, 2, 2024, 2, 1500.0)
        budget_service_with_stub.create_budget(2, 1, 2024, 1, 800.0)

        # Act
        user1_budgets = budget_service_with_stub.list_budgets(1)
        user2_budgets = budget_service_with_stub.list_budgets(2)

        # Assert
        assert len(user1_budgets) == 2
        assert len(user2_budgets) == 1
        assert all(b.user_id == 1 for b in user1_budgets)
        assert all(b.user_id == 2 for b in user2_budgets)

    # ===== TESTES COM MOCKS =====

    def test_create_budget_success_mock(
        self, budget_service_with_mock, mock_repository
    ):
        """Testa criação de orçamento com mock - verificando interações."""
        # Arrange
        mock_repository.list_by_user.return_value = []  # Nenhum orçamento existente
        mock_repository.create.return_value = None

        # Act
        budget_service_with_mock.create_budget(1, 1, 2024, 1, 1000.0)

        # Assert - verificar se métodos foram chamados corretamente
        mock_repository.list_by_user.assert_called_once_with(1)
        mock_repository.create.assert_called_once()

        # Verificar se o budget criado tem os valores corretos
        call_args = mock_repository.create.call_args[0][0]  # Primeiro argumento
        assert call_args.user_id == 1
        assert call_args.category_id == 1
        assert call_args.year == 2024
        assert call_args.month == 1
        assert call_args.limit_value == 1000.0

    def test_get_budget_success_mock(self, budget_service_with_mock, mock_repository):
        """Testa busca de orçamento com mock."""
        # Arrange
        mock_budget = Mock(spec=Budget)
        mock_budget.id = 1
        mock_repository.get.return_value = mock_budget

        # Act
        result = budget_service_with_mock.get_budget(1)

        # Assert
        assert result == mock_budget
        mock_repository.get.assert_called_once_with(1)

    def test_get_budget_not_found_mock(self, budget_service_with_mock, mock_repository):
        """Testa erro quando orçamento não é encontrado com mock."""
        # Arrange
        mock_repository.get.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="Budget not found"):
            budget_service_with_mock.get_budget(999)

    def test_update_budget_mock(self, budget_service_with_mock, mock_repository):
        """Testa atualização de orçamento com mock."""
        # Arrange
        mock_budget = Mock(spec=Budget)
        mock_repository.get.return_value = mock_budget
        mock_repository.update.return_value = None

        update_data = {"limit_value": 1500.0}

        # Act
        budget_service_with_mock.update_budget(1, update_data)

        # Assert
        mock_repository.get.assert_called_once_with(1)
        mock_repository.update.assert_called_once_with(1, update_data)

    def test_delete_budget_mock(self, budget_service_with_mock, mock_repository):
        """Testa exclusão de orçamento com mock."""
        # Arrange
        mock_budget = Mock(spec=Budget)
        mock_repository.get.return_value = mock_budget
        mock_repository.delete.return_value = True

        # Act
        budget_service_with_mock.delete_budget(1)

        # Assert
        mock_repository.get.assert_called_once_with(1)
        mock_repository.delete.assert_called_once_with(1)

    # ===== TESTES COMBINANDO MOCKS E STUBS =====

    def test_error_handling_with_stub_simulation(
        self, budget_service_with_stub, budget_repository_stub
    ):
        """Demonstra como usar stub para simular erros de infraestrutura."""
        # Arrange - configurar stub para simular erro
        budget_repository_stub.simulate_error("create")

        # Act & Assert
        with pytest.raises(RuntimeError, match="Erro de conexão com banco de dados"):
            budget_service_with_stub.create_budget(1, 1, 2024, 1, 1000.0)

    @patch("src.services.budget_service.Budget")
    def test_budget_creation_with_patch_mock(
        self, mock_budget_class, budget_service_with_mock, mock_repository
    ):
        """Demonstra uso de patch para mockar a classe Budget."""
        # Arrange
        mock_budget_instance = Mock()
        mock_budget_class.return_value = mock_budget_instance
        mock_repository.list_by_user.return_value = []
        mock_repository.create.return_value = None

        # Act
        budget_service_with_mock.create_budget(1, 1, 2024, 1, 1000.0)

        # Assert
        mock_budget_class.assert_called_once_with(
            id=None, user_id=1, category_id=1, year=2024, month=1, limit_value=1000.0
        )
        mock_repository.create.assert_called_once_with(mock_budget_instance)

    def test_side_effects_with_mock(self, budget_service_with_mock, mock_repository):
        """Demonstra uso de side_effects em mocks para simular comportamentos dinâmicos."""
        # Arrange - configurar side_effects para simular diferentes retornos
        mock_repository.list_by_user.side_effect = [
            [],  # Primeira chamada: nenhum orçamento
            [Mock(year=2024, month=1)],  # Segunda chamada: orçamento existente
        ]

        # Act & Assert
        # Primeira criação deve funcionar
        budget_service_with_mock.create_budget(1, 1, 2024, 1, 1000.0)

        # Segunda criação deve falhar (orçamento duplicado)
        with pytest.raises(
            ValueError, match="Já existe orçamento para este usuário neste mês"
        ):
            budget_service_with_mock.create_budget(1, 2, 2024, 1, 800.0)

        # Verificar que list_by_user foi chamado duas vezes
        assert mock_repository.list_by_user.call_count == 2


class TestMockVsStubComparison:
    """Classe para demonstrar as diferenças entre Mocks e Stubs."""

    def test_mock_behavior_verification(self):
        """Demonstra como mocks verificam comportamento (interações)."""
        # Arrange
        mock_repo = Mock()
        service = BudgetService(mock_repo)
        mock_repo.list_by_user.return_value = []

        # Act
        service.create_budget(1, 1, 2024, 1, 1000.0)

        # Assert - Mocks verificam COMO o código interage com dependências
        mock_repo.list_by_user.assert_called_once_with(1)
        mock_repo.create.assert_called_once()

    def test_stub_state_verification(self):
        """Demonstra como stubs verificam estado (resultados)."""
        # Arrange
        stub_repo = BudgetRepositoryStub()
        service = BudgetService(stub_repo)

        # Act
        budget = service.create_budget(1, 1, 2024, 1, 1000.0)

        # Assert - Stubs verificam O QUE aconteceu (estado final)
        assert budget.limit_value == 1000.0
        assert len(stub_repo.budgets) == 1
        assert stub_repo.budgets[1].user_id == 1
