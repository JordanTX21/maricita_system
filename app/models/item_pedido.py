from dataclasses import dataclass

@dataclass
class ItemPedido:
    producto_id: str
    nombre: str
    cantidad: int
    precio_unitario: float

    def subtotal(self) -> float:
        return round(self.cantidad * self.precio_unitario, 2)