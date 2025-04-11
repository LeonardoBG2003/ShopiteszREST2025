from datetime import datetime, date
from urllib import request

from dao.pedidosDAO import PedidoDAO
from fastapi import APIRouter, Request
from models.PedidoModel import Item, PedidoInsert, PedidoPay, Salida, PedidosSalida, Comprador, Vendedor, PedidoSelect

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

@router.post("/", response_model=Salida)
async def crearPedido(pedido: PedidoInsert, request: Request)->Salida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.agregar(pedido)

@router.put("/")
async def modificarPedido():
    return {"mensaje": "Modificando un pedido"}

@router.delete("/")
async def eliminarPedido():
    return {"mensaje": "Eliminando un pedido"}

@router.get("/", response_model=PedidosSalida)
async def consultaPedidos(request : Request)->PedidosSalida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.consultaGeneral()

@router.get("/{idPedido}")
async def consultarPedido(idPedido:str):
    return {"mensaje": "Consultando el pedido: "+idPedido}

@router.put("/{idPedido}/agregarProducto")
async def agregarProductoPedido(idPedido:str, item:Item):
    salida = {"mensaje":"Agregando un producto al pedido: " + idPedido, "item: ":item.dict()}
    return salida

@router.put("/{idPedido}/pagar", summary= "Pagar pedido", response_model=Salida)
async def pagarPedido(idPedido:str, pedidoPay:PedidoPay, request: Request):
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.pagarPedido(idPedido, pedidoPay)