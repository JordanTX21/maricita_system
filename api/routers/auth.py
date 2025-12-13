from fastapi import APIRouter, Depends, HTTPException
from api.schemas.auth import UserCreate, LoginRequest
from api.core.security import create_token
from api.deps import get_auth

router = APIRouter()

@router.post("/register")
def register(data: UserCreate, auth=Depends(get_auth)):
    auth.register(data.username, data.password)
    return {"message": "Usuario creado"}

@router.post("/login")
def login(data: LoginRequest, auth=Depends(get_auth)):
    if not auth.login(data.username, data.password):
        raise HTTPException(401, "Credenciales incorrectas")
    token = create_token({"sub": data.username})
    return {"access_token": token}
