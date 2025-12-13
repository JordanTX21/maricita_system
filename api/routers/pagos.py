from fastapi import APIRouter, Depends
from api.schemas.pago import PagoCreate
from api.deps import get_system

router = APIRouter()

@router.post("/")
def generar_pago(data: PagoCreate, system=Depends(get_system)):
    pago = system.generar_solicitud_pago(data.pedido_id, data.metodo)
    return pago.__dict__

@router.post("/{pedido_id}/confirmar")
def confirmar_pago(pedido_id: str, confirmar: bool, system=Depends(get_system)):
    system.verificar_pago(pedido_id, confirmar)
    return {"message": "Pago actualizado"}
