from pydantic import BaseModel
from datetime import datetime

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
    fechaRegistro: datetime | None = datetime.today()
    detalle: list[Item]

class Pago(BaseModel):
    fecha: datetime
    monto: float
    noTarjeta: str
    estatus: str

class PedidoPay(BaseModel):
    estatus: str | None = 'Pagado'
    pago:Pago

class Salida(BaseModel):
    estatus: str
    mensaje: str

class Comprador(BaseModel):
    idComprador: int
    nombre: str

class Vendedor(BaseModel):
    idVendedor: int
    nombre: str

class PedidoSelect(BaseModel):
    idPedido: str
    fechaRegistro: datetime
    fechaConfirmacion: datetime | None = None
    fechaCierre: datetime | None = None
    costosEnvio: float
    subtotal: float
    totalPagar: float
    estatus: str
    motivoCancelacion: str | None= None
    valoracion: int | None = None
    comprador: Comprador
    vendedor: Vendedor

class PedidosSalida(Salida):
    pedidos: list[PedidoSelect]

class PedidoCancelacion(BaseModel):
    motivoCancelacion: str

class Detalle(BaseModel):
    idProducto: int
    cantidad: int

class Envio(BaseModel):
    fechaSalida: datetime
    fechaEntPlan: datetime
    noGuia: str
    idPaqueteria: int
    detalle: list[Detalle]

class PedidoConfirmacion(BaseModel):
    fechaConfirmacion: datetime | None = None
    estatus: str | None = "Confirmado"
    envio: Envio

class Items(BaseModel):
    idProducto: int
    nombreProducto: str #Se agrega a diferencia de "Item"
    cantidad: int
    precio: float
    subtotal: float
    costoEnvio: float
    subtotalEnvio: float

class Pago2(BaseModel):
    idTarjeta: int | None = None     #Se agrega a diferencia de "Pago"
    noTarjeta: str
    fecha: datetime
    monto: float
    estatus: str

class Paqueteria(BaseModel):
    idPaqueteria: int
    nombre: str | None = None

class Envio2(BaseModel):    #En este metodo nuevo no hay detalle y en la paqueteria se agrego porque no viene el nombre
    fechaSalida: datetime
    fechaEntPlan: datetime
    fechaRecepcion: datetime | None = None #Tampoco tiene este campo
    noGuia: str
    paqueteria: Paqueteria | None = None

class Productos(BaseModel):
    idProducto: int
    nombreProducto: str
    cantidadEnviada: int
    cantidadRecibida: int | None = None
    comentario: str | None = None

class PedidoSelectID(BaseModel):
    idPedido: str
    fechaRegistro: datetime
    fechaConfirmacion: datetime | None = None
    fechaCierre: datetime | None = None
    costosEnvio: float
    subtotal: float
    totalPagar: float
    estatus: str
    motivoCancelacion: str | None = None
    valoracion: int | None = None
    items: list[Items]
    pago: Pago2
    comprador: Comprador
    vendedor: Vendedor
    envio: Envio2
    productos: list[Productos]
    paqueteria: Paqueteria

class PedidosSalidaID(Salida):
    pedido: PedidoSelectID | None = None

#1era parte del examen
class RegistrarEvento(BaseModel):
    evento: str
    lugar: str
    fecha: datetime

class EventoSalida(Salida):
    evento: RegistrarEvento | None = None

#2da parte del examen
class Tracking(BaseModel):
    evento: str
    lugar: str
    fecha: datetime

class DetalleEnvio(BaseModel):
    paqueteria: str
    noGuia: str
    tracking: list[Tracking] | None = None

class PedidoEnvio(BaseModel):
    idPedido: str
    envio: DetalleEnvio

class PedidoEnvioSalida(Salida):
    pedido: PedidoEnvio | None = None
