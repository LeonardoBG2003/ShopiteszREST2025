from fastapi import APIRouter
from models.PedidoModel import Item, PedidoInsert, Pago, PagoPedido

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

@router.post("/")
async def crearPedido(pedido: PedidoInsert):
    return {"mensaje": "Creando un pedido"}

@router.put("/")
async def modificarPedido():
    return {"mensaje": "Modificando un pedido"}

@router.delete("/")
async def eliminarPedido():
    return {"mensaje": "Eliminando un pedido"}

@router.get("/")
async def consultaPedidos():
    return {"mensaje": "Consultando los pedidos"}

@router.get("/{idPedido}")
async def consultarPedido(idPedido:str):
    return {"mensaje": "Consultando el pedido: "+idPedido}

@router.put("/{idPedido}/agregarProducto")
async def agregarProductoPedido(idPedido:str, item:Item):
    salida = {"mensaje":"Agregando un producto al pedido: "  + idPedido , "item: ":item.dict()}
    return salida

@router.put("/{idPedido}/pagar")
async def pagarPedido(idPedido:str, pagoPedido:PagoPedido):
    salida = {"mesaje": "Pagando el pedido: " + idPedido , PagoPedido: pagoPedido.dict()}