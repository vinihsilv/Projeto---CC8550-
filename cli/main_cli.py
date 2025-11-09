# cli/main_cli.py
from src.controllers.user_controller import UserController
from src.controllers.category_controller import CategoryController
from src.controllers.transaction_controller import TransactionController
from src.controllers.account_controller import AccountController
from src.controllers.budget_controller import BudgetController


def login_menu(user_controller):
    print("\n===== Login =====")
    email = input("E-mail: ")
    password = input("Senha: ")

    user = user_controller.login(email, password)
    if user:
        print(f"\nBem-vindo, {user.name}!")
        return user

    print("\nCredenciais inválidas.")
    return None


def category_menu(category_controller):
    while True:
        print("\n===== Menu de Categorias =====")
        print("1. Criar categoria")
        print("2. Listar categorias")
        print("3. Atualizar categoria")
        print("4. Deletar categoria")
        print("0. Voltar")

        op = input("Escolha: ")

        if op == "1":
            name = input("Nome da categoria: ")
            category_controller.create_category(name)

        elif op == "2":
            category_controller.list_categories()

        elif op == "3":
            cid = int(input("ID da categoria: "))
            new_name = input("Novo nome: ")
            category_controller.update_category(cid, new_name)

        elif op == "4":
            cid = int(input("ID da categoria: "))
            category_controller.delete_category(cid)

        elif op == "0":
            return

        else:
            print("Opção inválida.")


def transaction_menu(transaction_controller, logged_user_id):
    while True:
        print("\n===== Menu de Transações =====")
        print("1. Criar transação")
        print("2. Listar transações")
        print("3. Atualizar transação")
        print("4. Deletar transação")
        print("0. Voltar")

        op = input("Escolha: ")

        if op == "1":
            amount = float(input("Valor: "))
            description = input("Descrição: ")
            category_id = int(input("ID da categoria: "))
            transaction_controller.create_transaction(
                logged_user_id, amount, description, category_id
            )

        elif op == "2":
            transaction_controller.list_transactions(logged_user_id)

        elif op == "3":
            tid = int(input("ID da transação: "))
            amount = float(input("Novo valor: "))
            description = input("Nova descrição: ")
            category_id = int(input("Nova categoria: "))
            transaction_controller.update_transaction(
                tid, amount, description, category_id
            )

        elif op == "4":
            tid = int(input("ID da transação: "))
            transaction_controller.delete_transaction(tid)

        elif op == "0":
            return

        else:
            print("Opção inválida.")


def account_menu(account_controller, logged_user_id):
    while True:
        print("\n===== Menu de Contas =====")
        print("1. Criar conta")
        print("2. Listar contas")
        print("3. Atualizar conta")
        print("4. Deletar conta")
        print("0. Voltar")

        op = input("Escolha: ")

        if op == "1":
            name = input("Nome da conta: ")
            balance = float(input("Saldo inicial: "))
            account_controller.create_account(logged_user_id, name, balance)

        elif op == "2":
            account_controller.list_accounts(logged_user_id)

        elif op == "3":
            aid = int(input("ID da conta: "))
            new_name = input("Novo nome (ou enter para manter): ")
            new_balance_input = input("Novo saldo (ou enter para manter): ")
            new_balance = float(new_balance_input) if new_balance_input else None
            account_controller.update_account(aid, new_name or None, new_balance)

        elif op == "4":
            aid = int(input("ID da conta: "))
            account_controller.delete_account(aid)

        elif op == "0":
            return

        else:
            print("Opção inválida.")


def budget_menu(budget_controller, logged_user_id):
    while True:
        print("\n===== Menu de Orçamentos =====")
        print("1. Criar orçamento")
        print("2. Listar orçamentos")
        print("3. Atualizar orçamento")
        print("4. Deletar orçamento")
        print("0. Voltar")

        op = input("Escolha: ")

        if op == "1":
            category_id = int(input("ID da categoria: "))
            year = int(input("Ano do orçamento: "))
            limit_value = float(input("Valor limite: "))
            budget_controller.create_budget(
                logged_user_id, category_id, year, limit_value
            )

        elif op == "2":
            budget_controller.list_budgets(logged_user_id)

        elif op == "3":
            bid = int(input("ID do orçamento: "))
            new_category_id = input("Nova categoria (ou enter para manter): ")
            new_year = input("Novo ano (ou enter para manter): ")
            new_limit_value = input("Novo limite (ou enter para manter): ")
            budget_controller.update_budget(
                bid,
                category_id=int(new_category_id) if new_category_id else None,
                year=int(new_year) if new_year else None,
                limit_value=float(new_limit_value) if new_limit_value else None,
            )

        elif op == "4":
            bid = int(input("ID do orçamento: "))
            budget_controller.delete_budget(bid)

        elif op == "0":
            return

        else:
            print("Opção inválida.")


def main():
    user_controller = UserController()
    category_controller = CategoryController()
    transaction_controller = TransactionController()
    account_controller = AccountController()
    budget_controller = BudgetController()

    print("===== Bem-vindo ao Gerenciador Financeiro =====")

    logged_user = None

    # Loop de login
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
            user_controller.create_user(name, email, password)

        elif op == "0":
            print("Saindo...")
            return

        else:
            print("Opção inválida.")

    # Menu principal
    while True:
        print("\n===== Menu Principal =====")
        print("1. Categorias")
        print("2. Transações")
        print("3. Contas")
        print("4. Orçamentos")
        print("5. Logout")
        print("0. Sair")

        op = input("Escolha: ")

        if op == "1":
            category_menu(category_controller)

        elif op == "2":
            transaction_menu(transaction_controller, logged_user.id)

        elif op == "3":
            account_menu(account_controller, logged_user.id)

        elif op == "4":
            budget_menu(budget_controller, logged_user.id)

        elif op == "5":
            logged_user = None
            print("Logout realizado.")
            return main()  # reinicia fluxo

        elif op == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
