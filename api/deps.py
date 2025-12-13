from app.services.restaurante_service import RestauranteSystem
from app.services.auth_service import AuthService

system = RestauranteSystem()
auth_service = AuthService(system)

def get_system():
    return system

def get_auth():
    return auth_service
