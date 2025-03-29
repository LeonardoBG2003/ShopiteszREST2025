from pydantic import BaseModel
from datetime import date

class Item(BaseModel):
    idProducto: int
    cantidad: int
    precio: float
    subtotal: float
    costoEnvio: float
    subtotalEnvio: float

class PedidoInsert(BaseModel):
    idComprador : int
    idVendedor: int
    costosEnvio: float
    subtotal: float
    total: float
    estatus: str | None = 'Captura'
    detalle: list[Item]

class Pago(BaseModel):
    fecha: date
    monto: float
    noTarjeta: str
    estatus: str

class PagoPedido(BaseModel):
    estatus: str
    pago:list[Pago]
