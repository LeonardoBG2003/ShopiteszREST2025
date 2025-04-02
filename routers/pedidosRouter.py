from datetime import datetime, date

from fastapi import APIRouter
from models.PedidoModel import Item, PedidoInsert, PedidoPay, Salida, PedidosSalida, Comprador, Vendedor, PedidoSelect

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

@router.post("/", response_model=Salida)
async def crearPedido(pedido: PedidoInsert)->Salida:
    salida = Salida(estatus="OK", mensaje="Pedido creado con exito")
    #return {"mensaje": "Creando un pedido", "pedido": pedido}
    return salida

@router.put("/")
async def modificarPedido():
    return {"mensaje": "Modificando un pedido"}

@router.delete("/")
async def eliminarPedido():
    return {"mensaje": "Eliminando un pedido"}

@router.get("/", response_model=PedidosSalida)
async def consultaPedidos()->PedidosSalida:
    comprador = Comprador(idComprador=1, nombre="Juan")
    vendedor = Vendedor(idVendedor=1, nombre="WALMART")
    pedido = PedidoSelect(idPedido="500", fechaRegistro=datetime.today(),
                         fechaConfirmacion=datetime.today(), fechaCierre=datetime.today(),
                         costosEnvio=100, subtotal=200, totalPagar=3000, estatus="Pagado",
                         comprador=comprador, vendedor=vendedor)
    lista=[pedido]
    salida = PedidosSalida(estatus="OK", mensaje="Consulta de Pedidos", pedidos=lista)
    return salida

@router.get("/{idPedido}")
async def consultarPedido(idPedido:str):
    return {"mensaje": "Consultando el pedido: "+idPedido}

@router.put("/{idPedido}/agregarProducto")
async def agregarProductoPedido(idPedido:str, item:Item):
    salida = {"mensaje":"Agregando un producto al pedido: "  + idPedido , "item: ":item.dict()}
    return salida

@router.put("/{idPedido}/pagar")
async def pagarPedido(idPedido:str, pedidoPay:PedidoPay):
    salida = {"mesaje": "Pagando el pedido: " + idPedido , PedidoPay: PedidoPay.dict()}