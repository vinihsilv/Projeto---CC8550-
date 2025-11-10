from src.controllers.user_controller import UserController
from src.controllers.category_controller import CategoryController
from src.controllers.account_controller import AccountController
from src.controllers.budget_controller import BudgetController
from src.controllers.transaction_controller import TransactionController

from src.repositories.user_repository import UserRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.account_repository import AccountRepository
from src.repositories.budget_repository import BudgetRepository
from src.repositories.transaction_repository import TransactionRepository
from src.utils.database import SessionLocal


def login_menu(user_controller):
    print("\n===== Login =====")
    email = input("E-mail: ")
    password = input("Senha: ")

    try:
        user = user_controller.login(email, password)
        if user:
            print(f"\nBem-vindo, {user.name}!")
            return user
        print("\nCredenciais inválidas.")
        return None
    except ValueError as e:
        print(f"Erro: {e}")
        return None


def category_menu(category_controller, logged_user):
    while True:
        print("\n===== Menu de Categorias =====")
        print("1. Criar categoria")
        print("2. Listar categorias")
        print("3. Atualizar categoria")
        print("4. Deletar categoria")
        print("0. Voltar")
        op = input("Escolha: ")

        try:
            if op == "1":
                name = input("Nome: ")
                category_controller.create_category(name, logged_user.id)
                print("Categoria criada.")
            elif op == "2":
                categories = category_controller.list_categories(logged_user.id)
                if not categories:
                    print("Nenhuma categoria encontrada.")
                for c in categories:
                    print(f"ID: {c.id}, Nome: {c.name}")
            elif op == "3":
                cid = int(input("ID da categoria: "))
                new_name = input("Novo nome: ")
                category_controller.update_category(cid, {"name": new_name})
                print("Categoria atualizada.")
            elif op == "4":
                cid = int(input("ID da categoria: "))
                category_controller.delete_category(cid)
                print("Categoria deletada.")
            elif op == "0":
                return
            else:
                print("Opção inválida.")
        except ValueError as e:
            print(f"Erro: {e}")


def account_menu(account_controller, logged_user):
    while True:
        print("\n===== Menu de Contas =====")
        print("1. Criar conta")
        print("2. Listar contas")
        print("3. Atualizar conta")
        print("4. Deletar conta")
        print("0. Voltar")
        op = input("Escolha: ")

        try:
            if op == "1":
                name = input("Nome da conta: ")
                account_controller.create_account(name=name, user_id=logged_user.id)
                print("Conta criada.")
            elif op == "2":
                accounts = account_controller.list_accounts(logged_user.id)
                if not accounts:
                    print("Nenhuma conta encontrada.")
                for c in accounts:
                    print(f"ID: {c.id}, Nome: {c.name}, Saldo: {c.balance}")
            elif op == "3":
                aid = int(input("ID da conta: "))
                new_name = input("Novo nome (vazio para não alterar): ").strip() or None
                new_balance_input = input(
                    "Novo saldo (vazio para não alterar): "
                ).strip()
                new_balance = float(new_balance_input) if new_balance_input else None
                account_controller.update_account(
                    aid, name=new_name, balance=new_balance
                )
                print("Conta atualizada.")
            elif op == "4":
                aid = int(input("ID da conta: "))
                account_controller.delete_account(aid, logged_user.id)
                print("Conta deletada.")
            elif op == "0":
                return
            else:
                print("Opção inválida.")
        except ValueError as e:
            print(f"Erro: {e}")


def budget_menu(budget_controller, logged_user):
    while True:
        print("\n===== Menu de Budgets =====")
        print("1. Criar budget")
        print("2. Listar budgets")
        print("3. Atualizar budget")
        print("4. Deletar budget")
        print("0. Voltar")
        op = input("Escolha: ")

        try:
            if op == "1":
                category_id = int(input("ID da categoria: "))
                month = int(input("Mês (1-12): "))
                year = int(input("Ano: "))
                limit_value = float(input("Limite: "))
                budget_controller.create_budget(
                    user_id=logged_user.id,
                    category_id=category_id,
                    year=year,
                    month=month,
                    limit_value=limit_value,
                )
                print("Budget criado.")
            elif op == "2":
                budgets = budget_controller.list_budgets(logged_user.id)
                if not budgets:
                    print("Nenhum budget encontrado.")
                for b in budgets:
                    print(
                        f"ID: {b.id}, Categoria: {b.category_id}, Mês: {b.month}, "
                        f"Ano: {b.year}, Limite: {b.limit_value}"
                    )
            elif op == "3":
                bid = int(input("ID do budget: "))
                new_limit = float(input("Novo limite: "))
                budget_controller.update_budget(bid, {"limit_value": new_limit})
                print("Budget atualizado.")
            elif op == "4":
                bid = int(input("ID do budget: "))
                budget_controller.delete_budget(bid)
                print("Budget deletado.")
            elif op == "0":
                return
            else:
                print("Opção inválida.")
        except ValueError as e:
            print(f"Erro: {e}")


def transaction_menu(
    transaction_controller, logged_user, category_controller, account_controller
):
    while True:
        print("\n===== Menu de Transações =====")
        print("1. Criar transação")
        print("2. Listar transações")
        print("3. Atualizar transação")
        print("4. Deletar transação")
        print("5. Consultas Avançadas")
        print("6. Relatório de Resumo")
        print("0. Voltar")
        op = input("Escolha: ")

        try:
            if op == "1":
                categories = category_controller.list_categories(logged_user.id)
                for c in categories:
                    print(f"ID: {c.id}, Nome: {c.name}")

                account_id = int(input("ID da conta: "))
                category_id = int(input("ID da categoria: "))
                type_ = input("Tipo (income/expense): ").lower()
                amount = float(input("Valor: "))
                description = input("Descrição (opcional): ") or None

                transaction_controller.create_transaction(
                    user_id=logged_user.id,
                    amount=amount,
                    type_=type_,
                    account_id=account_id,
                    category_id=category_id,
                    description=description,
                )
                print("Transação criada com sucesso!")

            elif op == "2":
                transactions = transaction_controller.list_transactions(logged_user.id)
                if not transactions:
                    print("Nenhuma transação encontrada.")
                else:
                    for t in transactions:
                        print(
                            f"ID: {t.id}, Conta: {t.account_id}, Categoria: {t.category_id}, "
                            f"Tipo: {t.type}, Valor: {t.amount}, Data: {t.date}, Desc: {t.description}"
                        )

            elif op == "3":
                tx_id = int(input("ID da transação: "))
                new_amount = input("Novo valor (enter para manter): ")
                new_type = (
                    input("Novo tipo (income/expense, enter para manter): ").lower()
                    or None
                )
                new_category = input("Novo ID da categoria (enter para manter): ")
                new_desc = input("Nova descrição (enter para manter): ") or None

                data = {}
                if new_amount:
                    data["amount"] = float(new_amount)
                if new_type:
                    data["type_"] = new_type
                if new_category:
                    data["category_id"] = int(new_category)
                if new_desc:
                    data["description"] = new_desc

                transaction_controller.update_transaction(tx_id, logged_user.id, **data)
                print("Transação atualizada com sucesso!")

            elif op == "4":
                tx_id = int(input("ID da transação a deletar: "))
                transaction_controller.delete_transaction(tx_id, logged_user.id)
                print("Transação deletada com sucesso!")

            elif op == "5":
                advanced_search_menu(
                    transaction_controller,
                    logged_user,
                    category_controller,
                    account_controller,
                )

            elif op == "6":
                summary_report_menu(
                    transaction_controller,
                    logged_user,
                    category_controller,
                    account_controller,
                )

            elif op == "0":
                return
            else:
                print("Opção inválida.")
        except ValueError as e:
            print(f"Erro: {e}")


def advanced_search_menu(
    transaction_controller, logged_user, category_controller, account_controller
):
    """Menu para consultas avançadas de transações com filtros e ordenação."""
    from datetime import datetime

    while True:
        print("\n===== Consultas Avançadas =====")
        print("Filtros disponíveis:")
        print("1. Executar busca com filtros")
        print("0. Voltar")
        op = input("Escolha: ")

        if op == "1":
            try:
                print("\n--- Configurar Filtros (deixe em branco para não filtrar) ---")

                # Filtro por tipo
                transaction_type = (
                    input("Tipo (income/expense): ").strip().lower() or None
                )
                if transaction_type and transaction_type not in ["income", "expense"]:
                    transaction_type = None

                # Filtro por valores
                min_amount_input = input("Valor mínimo: ").strip()
                min_amount = float(min_amount_input) if min_amount_input else None

                max_amount_input = input("Valor máximo: ").strip()
                max_amount = float(max_amount_input) if max_amount_input else None

                # Filtro por datas
                print("Data de início (formato: YYYY-MM-DD):")
                start_date_input = input("Data início: ").strip()
                start_date = None
                if start_date_input:
                    try:
                        start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
                    except ValueError:
                        print(
                            "Formato de data inválido, ignorando filtro de data inicial"
                        )

                print("Data final (formato: YYYY-MM-DD):")
                end_date_input = input("Data final: ").strip()
                end_date = None
                if end_date_input:
                    try:
                        end_date = datetime.strptime(end_date_input, "%Y-%m-%d")
                    except ValueError:
                        print(
                            "Formato de data inválido, ignorando filtro de data final"
                        )

                # Filtro por categoria
                print("\n--- Categorias disponíveis ---")
                categories = category_controller.list_categories(logged_user.id)
                for c in categories:
                    print(f"ID: {c.id}, Nome: {c.name}")

                category_id_input = input("ID da categoria: ").strip()
                category_id = int(category_id_input) if category_id_input else None

                # Filtro por conta
                print("\n--- Contas disponíveis ---")
                accounts = account_controller.list_accounts(logged_user.id)
                for a in accounts:
                    print(f"ID: {a.id}, Nome: {a.name}")

                account_id_input = input("ID da conta: ").strip()
                account_id = int(account_id_input) if account_id_input else None

                # Filtro por descrição
                description_contains = input("Texto na descrição: ").strip() or None

                # Configurar ordenação
                print("\n--- Ordenação ---")
                print("Campos: date, amount, description, type")
                sort_by = input("Ordenar por (padrão: date): ").strip() or "date"

                print("Ordem: asc (crescente), desc (decrescente)")
                sort_order = input("Ordem (padrão: desc): ").strip() or "desc"

                # Executar busca
                results = transaction_controller.search_transactions_with_filters(
                    user_id=logged_user.id,
                    transaction_type=transaction_type,
                    min_amount=min_amount,
                    max_amount=max_amount,
                    start_date=start_date,
                    end_date=end_date,
                    category_id=category_id,
                    account_id=account_id,
                    description_contains=description_contains,
                    sort_by=sort_by,
                    sort_order=sort_order,
                )

                # Exibir resultados
                print(f"\n--- Resultados ({len(results)} transações encontradas) ---")
                if not results:
                    print("Nenhuma transação encontrada com os filtros especificados.")
                else:
                    for t in results:
                        print(
                            f"ID: {t.id} | Valor: R$ {t.amount:.2f} | Tipo: {t.type} | "
                            f"Data: {t.date.strftime('%d/%m/%Y')} | Conta: {t.account_id} | "
                            f"Categoria: {t.category_id} | Descrição: {t.description or 'N/A'}"
                        )

                input("\nPressione Enter para continuar...")

            except ValueError as e:
                print(f"Erro: {e}")
                input("Pressione Enter para continuar...")

        elif op == "0":
            return
        else:
            print("Opção inválida.")


def summary_report_menu(
    transaction_controller, logged_user, category_controller, account_controller
):
    """Menu para relatórios de resumo agrupados."""
    from datetime import datetime

    while True:
        print("\n===== Relatório de Resumo =====")
        print("1. Resumo por Categoria")
        print("2. Resumo por Conta")
        print("3. Resumo por Tipo")
        print("4. Resumo por Mês")
        print("0. Voltar")
        op = input("Escolha: ")

        if op in ["1", "2", "3", "4"]:
            try:
                # Mapear opção para grupo
                group_mapping = {
                    "1": "category",
                    "2": "account",
                    "3": "type",
                    "4": "month",
                }
                group_by = group_mapping[op]

                print(f"\n--- Configurar Relatório por {group_by.title()} ---")

                # Filtro de período
                print("Período (deixe em branco para todos os registros):")
                start_date_input = input("Data início (YYYY-MM-DD): ").strip()
                period_start = None
                if start_date_input:
                    try:
                        period_start = datetime.strptime(start_date_input, "%Y-%m-%d")
                    except ValueError:
                        print(
                            "Formato de data inválido, considerando todos os registros"
                        )

                end_date_input = input("Data final (YYYY-MM-DD): ").strip()
                period_end = None
                if end_date_input:
                    try:
                        period_end = datetime.strptime(end_date_input, "%Y-%m-%d")
                    except ValueError:
                        print(
                            "Formato de data inválido, considerando todos os registros"
                        )

                # Filtro por tipo de transação
                transaction_type = (
                    input("Filtrar por tipo (income/expense, ou vazio para ambos): ")
                    .strip()
                    .lower()
                    or None
                )
                if transaction_type and transaction_type not in ["income", "expense"]:
                    transaction_type = None

                # Ordenação
                print("\nOrdenar por: total_amount, count, avg_amount")
                sort_by = (
                    input("Ordenar por (padrão: total_amount): ").strip()
                    or "total_amount"
                )

                sort_order = input("Ordem asc/desc (padrão: desc): ").strip() or "desc"

                # Executar relatório
                results = transaction_controller.get_transactions_summary(
                    user_id=logged_user.id,
                    group_by=group_by,
                    period_start=period_start,
                    period_end=period_end,
                    transaction_type=transaction_type,
                    sort_by=sort_by,
                    sort_order=sort_order,
                )

                # Exibir resultados
                print(f"\n--- Relatório por {group_by.title()} ---")
                if not results:
                    print("Nenhum dado encontrado para o período especificado.")
                else:
                    print(f"{'Nome':<20} | {'Total':<12} | {'Qtd':<8} | {'Média':<12}")
                    print("-" * 60)

                    total_geral = 0
                    count_geral = 0

                    for item in results:
                        name = item["group_name"][
                            :18
                        ]  # Limitar nome para caber na coluna
                        total = item["total_amount"]
                        count = item["count"]
                        avg = item["avg_amount"]

                        print(
                            f"{name:<20} | R$ {total:>8.2f} | {count:>6} | R$ {avg:>8.2f}"
                        )

                        total_geral += total
                        count_geral += count

                    print("-" * 60)
                    avg_geral = total_geral / count_geral if count_geral > 0 else 0
                    print(
                        f"{'TOTAL GERAL':<20} | R$ {total_geral:>8.2f} | {count_geral:>6} | R$ {avg_geral:>8.2f}"
                    )

                input("\nPressione Enter para continuar...")

            except ValueError as e:
                print(f"Erro: {e}")
                input("Pressione Enter para continuar...")

        elif op == "0":
            return
        else:
            print("Opção inválida.")


def main():
    session = SessionLocal()
    transaction_repo = TransactionRepository(session)
    account_repo = AccountRepository(session)
    category_repo = CategoryRepository(session)
    budget_repo = BudgetRepository(session)
    user_repo = UserRepository(session)

    transaction_controller = TransactionController(
        transaction_repo, account_repo, category_repo, budget_repo
    )
    account_controller = AccountController(account_repo)
    budget_controller = BudgetController(budget_repo)
    user_controller = UserController(user_repo)
    category_controller = CategoryController(category_repo)

    logged_user = None

    while not logged_user:
        print("\n1. Login")
        print("2. Criar conta")
        print("0. Sair")
        op = input("Escolha: ")
        if op == "1":
            logged_user = login_menu(user_controller)
        elif op == "2":
            name = input("Nome: ")
            email = input("E-mail: ")
            password = input("Senha: ")
            try:
                user_controller.create_user(name, email, password)
                print("Conta criada.")
            except ValueError as e:
                print(f"Erro: {e}")
        elif op == "0":
            return
        else:
            print("Opção inválida.")

    while True:
        print("\n===== Menu Principal =====")
        print("1. Categorias")
        print("2. Contas")
        print("3. Budgets")
        print("4. Transações")
        print("5. Logout")
        print("0. Sair")
        op = input("Escolha: ")

        if op == "1":
            category_menu(category_controller, logged_user)
        elif op == "2":
            account_menu(account_controller, logged_user)
        elif op == "3":
            budget_menu(budget_controller, logged_user)
        elif op == "4":
            transaction_menu(
                transaction_controller,
                logged_user,
                category_controller,
                account_controller,
            )
        elif op == "5":
            logged_user = None
            print("Logout realizado.")
            return main()
        elif op == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
