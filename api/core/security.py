from datetime import datetime, timedelta
import jwt

SECRET_KEY = "maricita_secret"
ALGORITHM = "HS256"

def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=4)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
