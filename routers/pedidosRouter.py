from dao.pedidosDAO import PedidoDAO
from fastapi import APIRouter, Request, Depends
from models.pedidosModel import Item, PedidoInsert, PedidoPay, Salida, PedidosSalida, Comprador, Vendedor, PedidoSelect, \
    PedidoCancelacion, PedidoConfirmacion, PedidosSalidaID, RegistrarEvento, EventoSalida, PedidoEnvioSalida
from routers.usuariosRouter import validarUsuario
from models.usuariosModel import UsuarioSalida
router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

@router.post("/", response_model=Salida, summary="Crear un pedido")
async def crearPedido(pedido: PedidoInsert, request: Request)->Salida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.agregar(pedido)

@router.put("/")
async def modificarPedido():
    return {"mensaje": "Modificando un pedido"}

@router.delete("/{idPedido}/cancelar", response_model=Salida, summary="Cancelar un pedido")
async def eliminarPedido(idPedido: str, pedidoCancelacion:PedidoCancelacion, request: Request)->Salida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.cancelarPedido(idPedido, pedidoCancelacion)

@router.get("/", response_model=PedidosSalida)
async def consultaPedidos(request : Request, respuesta: UsuarioSalida = Depends(validarUsuario))->PedidosSalida:
    salida = PedidosSalida(estatus="", mensaje="", pedidos=[])
    usuario = respuesta.usuario
    if respuesta.estatus == "OK" and usuario['tipo'] == "Administrador":
        salida.estatus = "OK"
        salida.mensaje = "Listado de pedidos"
        pedidoDAO = PedidoDAO(request.app.db)
        return pedidoDAO.consultaGeneral()
    else:
        salida.estatus = "ERROR"
        salida.mensaje = "Sin autorizacion"
        return salida

#@router.get("/{idPedido}")
#async def consultarPedido(idPedido:str):
#    return {"mensaje": "Consultando el pedido: "+idPedido}

@router.put("/{idPedido}/agregarProducto")
async def agregarProductoPedido(idPedido:str, item:Item):
    salida = {"mensaje":"Agregando un producto al pedido: " + idPedido, "item: ":item.dict()}
    return salida

@router.put("/{idPedido}/pagar", response_model=Salida, summary= "Pagar pedido")
async def pagarPedido(idPedido: str, pedidoPay: PedidoPay, request: Request):
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.pagarPedido(idPedido, pedidoPay)

@router.put("/{idPedido}/confirmar", response_model=Salida, summary="Confirmar un pedido pagado")
async def confirmarPedido(idPedido: str, pedidoConfirmacion:PedidoConfirmacion, request: Request) -> Salida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.confirmarPedido(idPedido, pedidoConfirmacion)

@router.get("/{idPedido}", response_model=PedidosSalidaID, summary="Consultar un pedido por su ID")
async def consultarPedidoID(idPedido: str, request: Request) -> PedidosSalidaID:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.consultarPedidoPorID(idPedido)

@router.post("/{idPedido}/tracking", response_model=Salida, summary="Registrar el evento a un pedido")
async def registrarTracking(idPedido: str, evento: RegistrarEvento, request: Request) -> Salida:
    pedidoDAO = PedidoDAO(request.app.db)
    salida = pedidoDAO.registrarTracking(idPedido, evento)
    return Salida(estatus=salida.estatus, mensaje=salida.mensaje)

@router.get("/{idPedido}/tracking", response_model=PedidoEnvioSalida, summary="Consultar el tracking de un pedido")
async def trackingPedido(idPedido: str, request: Request) -> PedidoEnvioSalida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.trackingPedido(idPedido)
