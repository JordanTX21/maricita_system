from app.utils.hashing import hash_password, verify_password
from app.utils.excel_db import ExcelDB

class AuthService:
    def __init__(self, db: ExcelDB):
        self.db = db

    def register_user(self, username: str, password: str) -> bool:
        users = self.db.read("USUARIOS")

        # validar usuario existente
        if not users[users["username"] == username].empty:
            raise ValueError("El usuario ya existe")

        hashed = hash_password(password)

        self.db.append("USUARIOS", {
            "username": username,
            "password_hash": hashed
        })

        return True

    def login(self, username: str, password: str) -> bool:
        users = self.db.read("USUARIOS")

        user = users[users["username"] == username]

        if user.empty:
            return False

        hashed = user.iloc[0]["password_hash"]

        return verify_password(password, hashed)
