from src.controllers.user_controller import UserController
from src.controllers.category_controller import CategoryController
from src.controllers.account_controller import AccountController
from src.controllers.budget_controller import BudgetController
from src.controllers.transaction_controller import TransactionController


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


def category_menu(category_controller, logged_user):
    while True:
        print("\n===== Menu de Categorias =====")
        print("1. Criar categoria")
        print("2. Listar categorias")
        print("3. Atualizar categoria")
        print("4. Deletar categoria")
        print("0. Voltar")
        op = input("Escolha: ")

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
            category_controller.update_category(cid, new_name)
        elif op == "4":
            cid = int(input("ID da categoria: "))
            category_controller.delete_category(cid)
        elif op == "0":
            return
        else:
            print("Opção inválida.")


def account_menu(account_controller, logged_user):
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
            account_controller.create_account(user_id=logged_user.id, name=name)
        elif op == "2":
            account_controller.list_accounts(user_id=logged_user.id)
        elif op == "3":
            aid = input("ID da conta: ")
            new_name = input("Novo nome: ")
            account_controller.update_account(
                aid, user_id=logged_user.id, name=new_name
            )
        elif op == "4":
            aid = input("ID da conta: ")
            account_controller.delete_account(aid, logged_user.id)
        elif op == "0":
            return
        else:
            print("Opção inválida.")


def budget_menu(budget_controller, logged_user):
    while True:
        print("\n===== Menu de Budgets =====")
        print("1. Criar budget")
        print("2. Listar budgets")
        print("3. Atualizar budget")
        print("4. Deletar budget")
        print("0. Voltar")
        op = input("Escolha: ")

        if op == "1":
            category_id = int(input("ID da categoria: "))
            year = int(input("Ano: "))
            limit_value = float(input("Limite: "))
            budget_controller.create_budget(
                user_id=logged_user.id,
                category_id=category_id,
                year=year,
                limit_value=limit_value,
            )
        elif op == "2":
            budget_controller.list_budgets(user_id=logged_user.id)
        elif op == "3":
            bid = int(input("ID do budget: "))
            new_limit = float(input("Novo limite: "))
            budget_controller.update_budget(
                budget_id=bid, user_id=logged_user.id, limit_value=new_limit
            )
        elif op == "4":
            bid = int(input("ID do budget: "))
            budget_controller.delete_budget(budget_id=bid, user_id=logged_user.id)
        elif op == "0":
            return
        else:
            print("Opção inválida.")


def transaction_menu(transaction_controller, logged_user):
    while True:
        print("\n===== Menu de Transações =====")
        print("1. Criar transação")
        print("2. Listar transações")
        print("3. Atualizar transação")
        print("4. Deletar transação")
        print("0. Voltar")
        op = input("Escolha: ")

        if op == "1":
            try:
                amount = float(input("Valor: "))
                type_ = input("Tipo (income/expense): ").strip()
                account_id = int(input("ID da conta: "))
                category_id = int(input("ID da categoria: "))
                description = input("Descrição (opcional): ").strip() or None
                transaction_controller.create_transaction(
                    user_id=logged_user.id,
                    amount=amount,
                    type_=type_,
                    account_id=account_id,
                    category_id=category_id,
                    description=description,
                )
                print("Transação criada com sucesso!")
            except ValueError as e:
                print(f"Erro: {e}")
        elif op == "2":
            transactions = transaction_controller.list_transactions(
                user_id=logged_user.id
            )
            for t in transactions:
                print(
                    f"ID: {t.id}, Valor: {t.amount}, Tipo: {t.type}, Categoria: {t.category_id}, Data: {t.date}, Descrição: {t.description}"
                )
        elif op == "3":
            tid = int(input("ID da transação: "))
            amount_input = input("Novo valor (vazio para não alterar): ")
            type_input = input(
                "Novo tipo (income/expense, vazio para não alterar): "
            ).strip()
            category_input = input("Nova categoria (ID, vazio para não alterar): ")
            description_input = (
                input("Nova descrição (vazio para não alterar): ").strip() or None
            )

            transaction_controller.update_transaction(
                transaction_id=tid,
                user_id=logged_user.id,
                amount=float(amount_input) if amount_input else None,
                type_=type_input if type_input else None,
                category_id=int(category_input) if category_input else None,
                description=description_input,
            )
            print("Transação atualizada.")
        elif op == "4":
            tid = int(input("ID da transação: "))
            transaction_controller.delete_transaction(
                transaction_id=tid, user_id=logged_user.id
            )
            print("Transação deletada.")
        elif op == "0":
            return
        else:
            print("Opção inválida.")


def main():
    user_controller = UserController()
    category_controller = CategoryController()
    account_controller = AccountController()
    budget_controller = BudgetController()
    transaction_controller = TransactionController()

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
            print("Conta criada.")
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
            transaction_menu(transaction_controller, logged_user)
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
