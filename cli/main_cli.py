from src.controllers.user_controller import UserController
from src.controllers.category_controller import CategoryController
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


def main():
    user_controller = UserController()
    category_controller = CategoryController()
    transaction_controller = TransactionController()

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
        print("3. Logout")
        print("0. Sair")

        op = input("Escolha: ")

        if op == "1":
            category_menu(category_controller)

        elif op == "2":
            transaction_menu(transaction_controller)

        elif op == "3":
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
