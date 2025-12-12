from dataclasses import dataclass
from typing import Optional

@dataclass
class Cliente:
    id: str
    nombre: str
    telefono: str
    direccion: Optional[str] = None
    email: Optional[str] = None