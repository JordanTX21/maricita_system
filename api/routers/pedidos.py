from fastapi import APIRouter, Depends
from api.schemas.pedido import PedidoCreate
from api.deps import get_system

router = APIRouter()

@router.post("/")
def crear_pedido(data: PedidoCreate, system=Depends(get_system)):
    cliente = system.buscar_cliente_por_telefono(data.telefono_cliente)
    pedido = system.crear_pedido(cliente, data.items, data.tipo, data.direccion)
    return {"pedido_id": pedido.id, "total": pedido.total}

@router.post("/{pedido_id}/asignar")
def asignar(pedido_id: str, repartidor: str, system=Depends(get_system)):
    system.asignar_pedido(pedido_id, repartidor)
    return {"message": "Pedido asignado"}
