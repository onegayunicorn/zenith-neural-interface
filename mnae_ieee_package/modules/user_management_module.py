
"""
User Management Module
Manages user access and roles within the platform.
"""

class UserManagementModule:
    def __init__(self):
        self.users = {}
        self.roles = {"admin": [], "user": []}

    def register_user(self, username, password, role="user"):
        if username in self.users:
            return "User already exists"
        self.users[username] = {"password": password, "role": role}
        self.roles[role].append(username)
        print(f"User {username} registered with role {role}.")
        return "Registration successful"

    def login_user(self, username, password):
        user = self.users.get(username)
        if user and user["password"] == password:
            print(f"User {username} logged in.")
            return "Login successful"
        print("Invalid credentials.")
        return "Invalid credentials"

    def assign_role(self, username, role):
        if username not in self.users:
            return "User not found"
        old_role = self.users[username]["role"]
        self.roles[old_role].remove(username)
        self.users[username]["role"] = role
        self.roles[role].append(username)
        print(f"User {username} assigned role {role}.")
        return "Role assigned successfully"

    def has_permission(self, username, required_role):
        user = self.users.get(username)
        if user and user["role"] == required_role:
            return True
        return False
