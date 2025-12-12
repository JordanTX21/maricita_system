from dataclasses import dataclass
from typing import Optional

@dataclass
class Envio:
    tipo: str  # 'delivery' o 'salon'
    direccion: Optional[str] = None
    asignado_a: Optional[str] = None  # nombre del repartidor
    fecha_entrega_estimada: Optional[str] = None