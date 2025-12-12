from app.utils.hashing import hash_password, verify_password

class AuthService:
    def __init__(self, persistence):
        self.db = persistence

    def register_user(self, username, password):
        hashed = hash_password(password)
        self.db.save_user(username, {
            "user": username,
            "password": hashed
        })   # lo guardas en JSON
        return True

    def login(self, username, password):
        user = self.db.get_user(username)
        if not user:
            return False
        return verify_password(password, user["password"])
