from dataclasses import dataclass

@dataclass
class Producto:
    id: str
    nombre: str
    descripcion: str
    precio: float
    stock: int