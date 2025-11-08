from src.controllers.user_controller import UserController


def show_menu():
    print("\n=== USER MANAGEMENT CLI ===")
    print("1 - Create user")
    print("2 - List users")
    print("3 - Update user")
    print("4 - Delete user")
    print("0 - Exit")


def main():
    controller = UserController()

    while True:
        show_menu()
        option = input("Choose an option: ")

        if option == "1":
            name = input("Name: ")
            email = input("Email: ")
            password = input("Password: ")
            controller.create_user(name, email, password)

        elif option == "2":
            controller.list_users()

        elif option == "3":
            user_id = int(input("User ID to update: "))
            name = input("New name (or leave blank): ")
            email = input("New email (or leave blank): ")
            password = input("New password (or leave blank): ")
            data = {
                k: v
                for k, v in {"name": name, "email": email, "password": password}.items()
                if v
            }
            controller.update_user(user_id, data)

        elif option == "4":
            user_id = int(input("User ID to delete: "))
            controller.delete_user(user_id)

        elif option == "0":
            print("👋 Exiting...")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
