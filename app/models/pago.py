from dataclasses import dataclass
from typing import Optional

@dataclass
class Pago:
    id: str
    metodo: str  # 'tarjeta', 'efectivo', 'transferencia'
    monto: float
    confirmado: bool = False
    fecha: Optional[str] = None