# Diagramas do Projeto

Este diretório contém diagramas simples (Mermaid) representando as entidades e a arquitetura do projeto.

## Como visualizar

No VS Code, você pode visualizar Mermaid diretamente instalando a extensão "Markdown Preview Mermaid Support" ou usando o preview padrão do Markdown quando suportado.

- Abra os arquivos `.mmd` e use o preview de Markdown (Ctrl+Shift+V)
- Ou visualize os blocos Mermaid a seguir diretamente neste README

## Diagrama ER (Entidades e Relacionamentos)

```mermaid
%%{init: {"theme": "default"}}%%
classDiagram
    direction LR

    class User {
      +int id
      +string name
      +string email
      +string password
    }

    class Account {
      +int id
      +string name
      +float balance
      +int user_id
    }

    class Category {
      +int id
      +string name
      +int user_id
    }

    class Transaction {
      +int id
      +float amount
      +string type
      +DateTime date
      +int account_id
      +int category_id
      +string description
      +int user_id
    }

    class Budget {
      +int id
      +int user_id
      +int category_id
      +int year
      +int month
      +float limit_value
    }

    User "1" --> "*" Account : owns
    User "1" --> "*" Category : defines
    User "1" --> "*" Transaction : makes
    Category "1" --> "*" Transaction : classifies
    Account "1" --> "*" Transaction : records
    User "1" --> "*" Budget : sets
    Category "1" --> "*" Budget : scoped
```

## Arquitetura em Camadas

```mermaid
%%{init: {"theme": "default"}}%%
flowchart TD
    subgraph CLI[CLI / Interface Interativa]
        MCLI[main_cli.py]
    end

    subgraph Controllers[Camada de Controllers]
        UC[UserController]
        AC[AccountController]
        CC[CategoryController]
        BC[BudgetController]
        TC[TransactionController]
    end

    subgraph Services[Camada de Services]
        USvc[UserService]
        ASvc[AccountService]
        CSvc[CategoryService]
        BSvc[BudgetService]
        TSvc[TransactionService]
    end

    subgraph Repositories[Camada de Repositories]
        URepo[UserRepository]
        ARepo[AccountRepository]
        CRepo[CategoryRepository]
        BRepo[BudgetRepository]
        TRepo[TransactionRepository]
    end

    subgraph DB[Banco de Dados / SQLAlchemy]
        Base[(SQLAlchemy Base)]
    end

    MCLI --> UC & AC & CC & BC & TC
    UC --> USvc
    AC --> ASvc
    CC --> CSvc
    BC --> BSvc
    TC --> TSvc

    USvc --> URepo
    ASvc --> ARepo
    CSvc --> CRepo
    BSvc --> BRepo
    TSvc --> TRepo

    URepo --> Base
    ARepo --> Base
    CRepo --> Base
    BRepo --> Base
    TRepo --> Base
```

## Dicas

- Você pode exportar os diagramas para PNG/SVG usando ferramentas como `mmdc` (Mermaid CLI) ou extensões do VS Code.
- Para manter os diagramas atualizados, edite os arquivos `.mmd` conforme o modelo de dados evoluir.
