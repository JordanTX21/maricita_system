from pydantic import BaseModel

class PagoCreate(BaseModel):
    pedido_id: str
    metodo: str
