"""
Testes do AccountService utilizando stubs.

Este módulo demonstra o uso de stubs (objetos falsos com comportamento predefinido)
para testar a lógica de negócio do AccountService sem dependências reais.
"""

import pytest
from unittest.mock import Mock

from src.services.account_service import AccountService
from src.models.account import Account


class AccountRepositoryStub:
    """
    Stub do AccountRepository com comportamentos predefinidos.

    Um stub é um objeto falso que retorna valores específicos
    para métodos específicos, simulando diferentes cenários de teste.
    """

    def __init__(self):
        self.accounts = {}
        self.next_id = 1
        self.should_fail_create = False
        self.should_fail_update = False
        self.should_fail_delete = False

    def create(self, account: Account) -> Account:
        """Simula criação de conta."""
        if self.should_fail_create:
            raise Exception("Erro simulado na criação")

        account.id = self.next_id
        self.accounts[self.next_id] = account
        self.next_id += 1
        return account

    def list(self) -> list[Account]:
        """Simula listagem de contas."""
        return list(self.accounts.values())

    def get(self, account_id: int) -> Account | None:
        """Simula busca de conta por ID."""
        return self.accounts.get(account_id)

    def update(self, account_id: int, data: dict) -> Account | None:
        """Simula atualização de conta."""
        if self.should_fail_update:
            raise Exception("Erro simulado na atualização")

        account = self.accounts.get(account_id)
        if not account:
            return None

        for key, value in data.items():
            setattr(account, key, value)

        return account

    def delete(self, account_id: int) -> bool:
        """Simula exclusão de conta."""
        if self.should_fail_delete:
            raise Exception("Erro simulado na exclusão")

        if account_id in self.accounts:
            del self.accounts[account_id]
            return True
        return False

    def set_failure_mode(self, create=False, update=False, delete=False):
        """Configura o stub para simular falhas."""
        self.should_fail_create = create
        self.should_fail_update = update
        self.should_fail_delete = delete


class TestAccountServiceStubs:
    """Testes do AccountService usando stubs."""

    @pytest.fixture
    def repository_stub(self):
        """Fixture que cria um stub do repositório."""
        return AccountRepositoryStub()

    @pytest.fixture
    def account_service(self, repository_stub):
        """Fixture que cria o AccountService com repositório stub."""
        return AccountService(repository=repository_stub)

    def test_create_account_success(self, account_service, repository_stub):
        """Testa criação de conta com sucesso usando stub."""
        # Act
        account = account_service.create_account("Conta Corrente", user_id=1)

        # Assert
        assert account.id == 1
        assert account.name == "Conta Corrente"
        assert account.user_id == 1
        assert account.balance == 0.0
        assert len(repository_stub.accounts) == 1

    def test_create_account_failure(self, account_service, repository_stub):
        """Testa falha na criação de conta."""
        # Arrange - configurar stub para falhar
        repository_stub.set_failure_mode(create=True)

        # Act & Assert
        with pytest.raises(Exception, match="Erro simulado na criação"):
            account_service.create_account("Conta Teste", user_id=1)

    def test_list_accounts_by_user(self, account_service, repository_stub):
        """Testa listagem de contas filtrada por usuário."""
        # Arrange - criar contas para diferentes usuários
        account_service.create_account("Conta User 1", user_id=1)
        account_service.create_account("Conta User 1 - 2", user_id=1)
        account_service.create_account("Conta User 2", user_id=2)

        # Act
        user1_accounts = account_service.list_accounts(user_id=1)
        user2_accounts = account_service.list_accounts(user_id=2)

        # Assert
        assert len(user1_accounts) == 2
        assert len(user2_accounts) == 1
        assert all(acc.user_id == 1 for acc in user1_accounts)
        assert all(acc.user_id == 2 for acc in user2_accounts)

    def test_list_accounts_empty(self, account_service):
        """Testa listagem quando não há contas."""
        # Act
        accounts = account_service.list_accounts(user_id=1)

        # Assert
        assert len(accounts) == 0

    def test_get_account_success(self, account_service, repository_stub):
        """Testa busca de conta existente."""
        # Arrange
        created_account = account_service.create_account("Conta Teste", user_id=1)

        # Act
        found_account = account_service.get_account(created_account.id)

        # Assert
        assert found_account.id == created_account.id
        assert found_account.name == "Conta Teste"

    def test_get_account_not_found(self, account_service):
        """Testa erro quando conta não é encontrada."""
        # Act & Assert
        with pytest.raises(ValueError, match="Account not found"):
            account_service.get_account(999)

    def test_update_account_name_only(self, account_service, repository_stub):
        """Testa atualização apenas do nome da conta."""
        # Arrange
        account = account_service.create_account("Nome Original", user_id=1)

        # Act
        account_service.update_account(account.id, name="Nome Atualizado")

        # Assert
        updated_account = repository_stub.get(account.id)
        assert updated_account.name == "Nome Atualizado"
        assert updated_account.balance == 0.0  # Balance não alterado

    def test_update_account_balance_only(self, account_service, repository_stub):
        """Testa atualização apenas do saldo da conta."""
        # Arrange
        account = account_service.create_account("Conta Teste", user_id=1)

        # Act
        account_service.update_account(account.id, balance=1500.0)

        # Assert
        updated_account = repository_stub.get(account.id)
        assert updated_account.name == "Conta Teste"  # Nome não alterado
        assert updated_account.balance == 1500.0

    def test_update_account_both_fields(self, account_service, repository_stub):
        """Testa atualização de nome e saldo simultaneamente."""
        # Arrange
        account = account_service.create_account("Nome Original", user_id=1)

        # Act
        account_service.update_account(account.id, name="Novo Nome", balance=2000.0)

        # Assert
        updated_account = repository_stub.get(account.id)
        assert updated_account.name == "Novo Nome"
        assert updated_account.balance == 2000.0

    def test_update_account_no_data(self, account_service):
        """Testa erro quando nenhum dado é fornecido para atualização."""
        # Act & Assert
        with pytest.raises(ValueError, match="Nenhum dado para atualizar"):
            account_service.update_account(1)

    def test_update_account_failure(self, account_service, repository_stub):
        """Testa falha na atualização de conta."""
        # Arrange
        account = account_service.create_account("Conta Teste", user_id=1)
        repository_stub.set_failure_mode(update=True)

        # Act & Assert
        with pytest.raises(Exception, match="Erro simulado na atualização"):
            account_service.update_account(account.id, name="Novo Nome")

    def test_delete_account_success(self, account_service, repository_stub):
        """Testa exclusão de conta com sucesso."""
        # Arrange
        account = account_service.create_account("Conta Para Deletar", user_id=1)

        # Act
        account_service.delete_account(account.id, user_id=1)

        # Assert
        assert repository_stub.get(account.id) is None

    def test_delete_account_not_found(self, account_service):
        """Testa erro ao deletar conta inexistente."""
        # Act & Assert
        with pytest.raises(
            ValueError, match="Conta não encontrada ou pertence a outro usuário"
        ):
            account_service.delete_account(999, user_id=1)

    def test_delete_account_wrong_user(self, account_service, repository_stub):
        """Testa erro ao deletar conta de outro usuário."""
        # Arrange
        account = account_service.create_account("Conta User 1", user_id=1)

        # Act & Assert
        with pytest.raises(
            ValueError, match="Conta não encontrada ou pertence a outro usuário"
        ):
            account_service.delete_account(account.id, user_id=2)  # Usuário diferente

    def test_delete_account_failure(self, account_service, repository_stub):
        """Testa falha na exclusão de conta."""
        # Arrange
        account = account_service.create_account("Conta Teste", user_id=1)
        repository_stub.set_failure_mode(delete=True)

        # Act & Assert
        with pytest.raises(Exception, match="Erro simulado na exclusão"):
            account_service.delete_account(account.id, user_id=1)


class TestAccountServiceStubScenarios:
    """Testes de cenários específicos usando stubs configuráveis."""

    def test_repository_behavior_simulation(self):
        """Demonstra como stubs podem simular diferentes comportamentos de repositório."""
        # Arrange
        stub = AccountRepositoryStub()
        service = AccountService(stub)

        # Scenario 1: Operação normal
        account = service.create_account("Conta Normal", user_id=1)
        assert account.id == 1

        # Scenario 2: Simular falha na criação
        stub.set_failure_mode(create=True)
        with pytest.raises(Exception):
            service.create_account("Conta Falha", user_id=1)

        # Scenario 3: Voltar ao funcionamento normal
        stub.set_failure_mode(create=False)
        account2 = service.create_account("Conta Normal 2", user_id=1)
        assert account2.id == 2

    def test_multiple_users_scenario(self):
        """Testa cenário com múltiplos usuários e contas."""
        # Arrange
        stub = AccountRepositoryStub()
        service = AccountService(stub)

        # Act - criar contas para diferentes usuários
        accounts_user1 = []
        accounts_user2 = []

        for i in range(3):
            acc1 = service.create_account(f"User1-Account{i}", user_id=1)
            acc2 = service.create_account(f"User2-Account{i}", user_id=2)
            accounts_user1.append(acc1)
            accounts_user2.append(acc2)

        # Assert - verificar isolamento entre usuários
        user1_list = service.list_accounts(user_id=1)
        user2_list = service.list_accounts(user_id=2)

        assert len(user1_list) == 3
        assert len(user2_list) == 3
        assert all("User1" in acc.name for acc in user1_list)
        assert all("User2" in acc.name for acc in user2_list)
