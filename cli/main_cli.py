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
            print("Conta criada.")
        elif op == "2":
            account_controller.list_accounts(user_id=logged_user.id)
            print("Contas listadas.")
            for c in account_controller.list_accounts(user_id=logged_user.id):
                print(f"ID: {c.id}, Nome: {c.name}, Saldo: {c.balance}")
        elif op == "3":
            aid = int(input("ID da conta: "))
            new_name = input("Novo nome (vazio para não alterar): ").strip() or None
            new_balance_input = input("Novo saldo (vazio para não alterar): ").strip()
            new_balance = float(new_balance_input) if new_balance_input else None

            account_controller.update_account(
                account_id=aid, name=new_name, balance=new_balance
            )
            print("Conta atualizada.")
        elif op == "4":
            aid = int(input("ID da conta: "))
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
        elif op == "2":
            print("Budgets listados.")
            for b in budget_controller.list_budgets(user_id=logged_user.id):
                print(
                    f"ID: {b.id}, Categoria: {b.category_id}, Mês: {b.month}, Ano: {b.year}, Limite: {b.limit_value}"
                )
        elif op == "3":
            bid = int(input("ID do budget: "))
            new_limit = float(input("Novo limite: "))
            budget_controller.update_budget(
                budget_id=bid, data={"limit_value": new_limit}
            )
        elif op == "4":
            bid = int(input("ID do budget: "))
            budget_controller.delete_budget(budget_id=bid)
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
            account_id = int(input("ID da conta: "))
            category_id = int(input("ID da categoria: "))
            type_ = input("Tipo (income/expense): ").lower()
            amount = float(input("Valor: "))
            description = input("Descrição (opcional): ") or None

            try:
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
            transactions = transaction_controller.list_transactions(logged_user.id)
            if not transactions:
                print("Nenhuma transação encontrada.")
            else:
                print("\nTransações listadas:")
                for t in transactions:
                    account_id = getattr(t, "account_id", "N/A")
                    print(
                        f"ID: {t.id}, Conta: {account_id}, Categoria: {t.category_id}, "
                        f"Tipo: {t.type}, Valor: {t.amount}, Data: {t.date}, Desc: {t.description}"
                    )

        elif op == "3":
            tx_id = int(input("ID da transação: "))
            print("Preencha apenas os campos que deseja atualizar:")
            new_amount = input("Novo valor (enter para manter): ")
            new_type = (
                input("Novo tipo (income/expense, enter para manter): ").lower() or None
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

            try:
                transaction_controller.update_transaction(
                    transaction_id=tx_id, user_id=logged_user.id, **data
                )
                print("Transação atualizada com sucesso!")
            except ValueError as e:
                print(f"Erro: {e}")

        elif op == "4":
            tx_id = int(input("ID da transação a deletar: "))
            try:
                transaction_controller.delete_transaction(tx_id, logged_user.id)
                print("Transação deletada com sucesso!")
            except ValueError as e:
                print(f"Erro: {e}")

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
