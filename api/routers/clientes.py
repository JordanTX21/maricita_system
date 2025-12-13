from fastapi import APIRouter, Depends
from api.schemas.cliente import ClienteCreate
from api.deps import get_system

router = APIRouter()

@router.post("/")
def crear_cliente(data: ClienteCreate, system=Depends(get_system)):
    cliente = system.crear_cliente(data.nombre, data.telefono, data.direccion)
    return {"id": cliente.id}
