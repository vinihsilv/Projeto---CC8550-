from src.controllers.user_controller import UserController
from src.controllers.category_controller import CategoryController
from src.controllers.transaction_controller import TransactionController
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
            cid = input("ID da categoria: ")
            new_name = input("Novo nome: ")
            category_controller.update_category(cid, new_name)

        elif op == "4":
            cid = input("ID da categoria: ")
            category_controller.delete_category(cid)

        elif op == "0":
            return

        else:
            print("Opção inválida.")


def transaction_menu(transaction_controller):
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
            category_id = input("ID da categoria: ")
            transaction_controller.create_transaction(amount, description, category_id)

        elif op == "2":
            transaction_controller.list_transactions()

        elif op == "3":
            tid = input("ID da transação: ")
            amount = float(input("Novo valor: "))
            description = input("Nova descrição: ")
            category_id = input("Nova categoria: ")
            transaction_controller.update_transaction(
                tid, amount, description, category_id
            )

        elif op == "4":
            tid = input("ID da transação: ")
            transaction_controller.delete_transaction(tid)

        elif op == "0":
            return

        else:
            print("Opção inválida.")


def budget_menu(budget_controller):
    while True:
        print("\n===== Menu de Orçamentos =====")
        print("1. Criar orçamento")
        print("2. Listar orçamentos")
        print("3. Atualizar orçamento")
        print("4. Deletar orçamento")
        print("0. Voltar")

        op = input("Escolha: ")

        if op == "1":
            category_id = input("ID da categoria: ")
            year = int(input("Ano (YYYY): "))
            month = int(input("Mês (1-12): "))
            limit_value = float(input("Valor limite: "))

            budget_controller.create_budget(category_id, year, month, limit_value)

        elif op == "2":
            budget_controller.list_budgets()

        elif op == "3":
            bid = input("ID do orçamento: ")

            print("Deixe em branco para não alterar")
            category_id = input("Nova categoria: ")
            year = input("Novo ano: ")
            month = input("Novo mês: ")
            limit_value = input("Novo limite: ")

            budget_controller.update_budget(
                bid,
                category_id if category_id else None,
                int(year) if year else None,
                int(month) if month else None,
                float(limit_value) if limit_value else None,
            )

        elif op == "4":
            bid = input("ID do orçamento: ")
            budget_controller.delete_budget(bid)

        elif op == "0":
            return

        else:
            print("Opção inválida.")


def main():
    user_controller = UserController()
    category_controller = CategoryController()
    transaction_controller = TransactionController()
    budget_controller = BudgetController()

    print("===== Bem-vindo ao Gerenciador Financeiro =====")

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
            user_controller.create_user(name, email, password)

        elif op == "0":
            print("Saindo...")
            return

        else:
            print("Opção inválida.")

    while True:
        print("\n===== Menu Principal =====")
        print("1. Categorias")
        print("2. Transações")
        print("3. Orçamentos")
        print("4. Logout")
        print("0. Sair")

        op = input("Escolha: ")

        if op == "1":
            category_menu(category_controller)

        elif op == "2":
            transaction_menu(transaction_controller)

        elif op == "3":
            budget_menu(budget_controller)

        elif op == "4":
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
