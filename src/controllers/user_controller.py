from src.services.user_service import UserService


class UserController:
    """Controller to manage user actions between CLI and service."""

    def __init__(self):
        self.service = UserService()

    def create_user(self, name: str, email: str, password: str):
        try:
            self.service.create_user(name, email, password)
            print("User created successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def list_users(self):
        users = self.service.list_users()
        if not users:
            print("No users found.")
            return
        print("\n--- Registered Users ---")
        for u in users:
            print(f"ID: {u.id} | Name: {u.name} | Email: {u.email}")

    def login(self, email, password):
        user = self.service.authenticate(email, password)
        return user

    def update_user(self, user_id: int, data: dict):
        try:
            self.service.update_user(user_id, data)
            print("User updated successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def delete_user(self, user_id: int):
        try:
            self.service.delete_user(user_id)
            print("User deleted successfully.")
        except ValueError as e:
            print(f"Error: {e}")
