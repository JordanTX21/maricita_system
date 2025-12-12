from dataclasses import dataclass
from typing import Optional, List
from app.models.pago import Pago
from app.models.envio import Envio
from app.models.item_pedido import ItemPedido

@dataclass
class Pedido:
    id: str
    cliente_id: str
    items: List[ItemPedido]
    total: float
    estado: str  # pendiente, en_proceso, entregado, cancelado
    tipo_atencion: str  # delivery / salon
    pago: Optional[Pago]
    envio: Optional[Envio]
    creado_en: str