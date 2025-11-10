# Projeto CC8550 — Gerenciador Financeiro

Camadas: CLI → Controllers → Services → Repositories → Database (SQLAlchemy). Banco SQLite por padrão.

Luan Petroucic Moreno – RA: 22.122.076‑7
Vinicius Henrique Silva – RA: 22.122.063‑5
Cauê Jacomini Zanatti – RA: 22.122.024‑7
Giulliano Mazzaro Camargo – RA: 22.121.024‑8

## Sumário
- Visão geral
- Pré‑requisitos e setup
- Como rodar (CLI)
- Configuração de banco e logs
- Roteiro de testes
- Critério de aceitação
- Benchmarks (performance)
- Diagrama(s)
- Estrutura de pastas

## Visão geral
Aplicação acadêmica para gerenciar contas, categorias, transações e orçamentos, com arquitetura em camadas e suíte de testes completa (unit, functional, integration, mocks/stubs e performance).

Principais recursos
- CRUD de Usuários, Contas, Categorias, Transações e Orçamentos
- Regras de negócio (saldo insuficiente, orçamento excedido, validação de pertencimento)
- Consultas avançadas com filtros e ordenação (por tipo, valor, data, conta, categoria, descrição)
- Relatórios/resumos agrupados (por categoria, conta, tipo, mês) com totais e médias
- CLI interativa para operações comuns e consultas

## Pré‑requisitos e setup
- Windows
- Python 3.11+ (recomendado 3.13)
- Virtual env (venv) no projeto

Criar/ativar venv (PowerShell):
```powershell
python -m venv .\venv
.\venv\Scripts\Activate.ps1
python -m pip install -r config\requirements.txt
```

## Como rodar (CLI)
```powershell
.\venv\Scripts\python.exe cli\main_cli.py
```

Funcionalidades do CLI (atalhos principais)
- Gerenciar contas/categorias/transações
- Busca avançada de transações (filtrar por período, tipo, conta, categoria, etc.)
- Relatório/resumo por categoria/conta/tipo/mês

## Configuração de banco e logs
- Banco: `sqlite:///db.sqlite` (arquivo na raiz), configurado em `src\utils\database.py`.
- SQL echo (logs SQLAlchemy): desativado por padrão. Ative temporariamente:
```powershell
$env:SQL_ECHO = "true"
.\venv\Scripts\python.exe -m pytest -q
Remove-Item Env:SQL_ECHO
```

## Roteiro de testes
Ativar venv:
```powershell
.\venv\Scripts\Activate.ps1
```
Rodar tudo:
```powershell
.\venv\Scripts\python.exe -m pytest -q
```
Por tipo:
```powershell
# Unit
.\venv\Scripts\python.exe -m pytest -q test\units
# Funcional
.\venv\Scripts\python.exe -m pytest -q test\functional
# Integração
.\venv\Scripts\python.exe -m pytest -q test\integration
# Mocks e Stubs
.\venv\Scripts\python.exe -m pytest -q test\mocks_and_stubs
# Performance (benchmarks)
.\venv\Scripts\python.exe -m pytest -q test\performance
```
Somente mocks/stubs:
```powershell
.\venv\Scripts\python.exe -m pytest -q test\mocks_and_stubs
```
Cobertura de código:
```powershell
.\venv\Scripts\python.exe -m pytest --cov=src --cov-report=term-missing --cov-report=html
start .\htmlcov\index.html
```
Coleta e filtros úteis:
```powershell
.\venv\Scripts\python.exe -m pytest --collect-only -q
.\venv\Scripts\python.exe -m pytest -q test\functional\test_functional.py
.\venv\Scripts\python.exe -m pytest -q test\functional\test_functional.py::test_func_registro_transacao
.\venv\Scripts\python.exe -m pytest -q -k "transaction and not integration"
.\venv\Scripts\python.exe -m pytest -q --last-failed
```

## Critério de aceitação
O critério de aceitação principal é: todos os testes (unitários, funcionais, integração, mocks/stubs e performance) devem finalizar sem falhas (0 failed). Qualquer falha impede a aceitação.

## Benchmarks (performance)
Rodar benchmarks:
```powershell
.\venv\Scripts\python.exe -m pytest -q test\performance
```
Salvar e comparar:
```powershell
.\venv\Scripts\python.exe -m pytest test\performance --benchmark-save=run1
.\venv\Scripts\python.exe -m pytest test\performance --benchmark-compare=run1
```

## Diagrama(s)
Arquivos Mermaid em `docs\diagrams`:
- ER: `docs/diagrams/er.mmd`
- Arquitetura: `docs/diagrams/architecture.mmd`

Para visualizar no VS Code, instale uma extensão Mermaid e abra os arquivos `.mmd`.

## Estrutura de pastas (resumo)
```
cli/
config/
docs/
src/
  controllers/ services/ repositories/ models/ utils/
test/
  units/ functional/ integration/ mocks_and_stubs/ performance/
```

## Dicas e solução de problemas
- SQLAlchemy imprimindo SQL no console? Por padrão está desativado; ver seção "Configuração de banco e logs" para ativar/desativar via `SQL_ECHO`.
- Dependências: reinstale com `python -m pip install -r config/requirements.txt` dentro do venv.
- Erros de permissão ao ativar venv: execute o PowerShell como Administrador ou ajuste a ExecutionPolicy.
