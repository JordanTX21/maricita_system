from pydantic import BaseModel
from typing import List

class ItemPedido(BaseModel):
    producto_id: str
    cantidad: int

class PedidoCreate(BaseModel):
    telefono_cliente: str
    items: List[ItemPedido]
    tipo: str
    direccion: str | None = None
