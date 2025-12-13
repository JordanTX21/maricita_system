from pydantic import BaseModel

class ProductoResponse(BaseModel):
    id: str
    nombre: str
    precio: float
    stock: int
