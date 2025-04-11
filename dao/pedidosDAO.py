from models.PedidoModel import PedidoInsert, Salida, PedidosSalida, PedidoPay
from datetime import datetime
from dao.usuariosDAO import UsuarioDAO
from fastapi.encoders import jsonable_encoder
from bson import ObjectId


class PedidoDAO:
    def __init__(self, db):
        self.db = db

    def agregar(self, pedido: PedidoInsert):
        salida = Salida(estatus="", mensaje="")
        try:
            pedido.fechaRegistro = datetime.today()
            if pedido.idVendedor != pedido.idComprador:
                usuarioDAO = UsuarioDAO(self.db)
                if usuarioDAO.comprobarUsuario(pedido.idComprador) and usuarioDAO.comprobarUsuario(pedido.idVendedor):
                    result = self.db.pedidos.insert_one(jsonable_encoder(pedido))
                    salida.estatus = "OK"
                    salida.mensaje = "Pedido agregado con exito con id: " + str(result.inserted_id)
                else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "El usuario comprador o el vendedor no existen o no se encuentran activos."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se pudo agregar el pedido, porque los ids de los usuarios son iguales."
        except Exception as ex:
            print(ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al agregar el pedido, consulta al adminstrador."
        return salida

    def consultaGeneral(self):
        salida = PedidosSalida(estatus="", mensaje="", pedidos=[])
        try:
            lista = list(self.db.pedidosView.find())
            salida.estatus = "OK"
            salida.mensaje = "Listado de pedidos."
            salida.pedidos = lista
        except Exception as ex:
            print(ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consulta los pedidos, consulta al adminstrador."
        return salida

    def evaluarPedido(self, idPedido: str):
        pedido = None
        try:
            pedido = self.db.pedidosView.find_one({"idPedido": idPedido, "estatus": "Captura"})
        except Exception as ex:
            print(ex)
        return pedido

    def pagarPedido(self, idPedido: str, pedidoPay: PedidoPay):
        salida = Salida(estatus="", mensaje="")
        try:
            pedido = self.evaluarPedido(idPedido)
            if pedido:
                usuarioDAO = UsuarioDAO(self.db)
                if usuarioDAO.comprobarTarjeta(pedido['comprador'].get("idComprador"), pedidoPay.pago.noTarjeta) == 1:
                    if pedido['total'] == pedidoPay.pago.monto and pedidoPay.pago.estatus == "Autorizado":
                        pedidoPay.estatus = "Pagado"
                        self.db.pedidos.update_one({"_id": ObjectId(idPedido)},
                                                   {"$set": {"pago": jsonable_encoder(pedidoPay.pago),
                                                             "estatus": pedidoPay.estatus}})
                        salida.estatus = "OK"
                        salida.mensaje = f"El pedido con id: {idPedido} fue pagado con exito"
                    else:
                        salida.estatus = "ERROR"
                        salida.mensaje = "El pedido no se puede pagar debido a que no se cubre el monto total a pagar"
                else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "El pedido no se puede pagar debido a que la tarjeta no existe o no pertenece al comprador"
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El pedido no existe o no se encuentra en captura"
        except Exception as ex:
            print(ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al pagar el pedido, consulta al adminstrador"
        return salida