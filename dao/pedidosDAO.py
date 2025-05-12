from models.pedidosModel import PedidoInsert, Salida, PedidosSalida, PedidoPay, PedidoCancelacion, PedidoConfirmacion, PedidosSalidaID, EventoSalida, RegistrarEvento, PedidoEnvioSalida
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

    def consultarEstatusPedido(self, idPedido: str):
        estatus = None
        try:
            estatus = self.db.pedidosView.find_one({"idPedido": idPedido}, projection={"estatus": True})
        except Exception as ex:
            print(ex)
        return estatus

    def cancelarPedido(self, idPedido: str, pedidoCancelacion: PedidoCancelacion):
        salida = Salida(estatus="", mensaje="")
        try:
            objeto = self.consultarEstatusPedido(idPedido)
            if objeto["estatus"] == "Captura":
                self.db.pedidos.update_one({"idPedido":idPedido},
                                            {"$set": {"estatus": "Cancelado", "motivoCancelacion": pedidoCancelacion.motivoCancelacion}})
                salida.estatus = "OK"
                salida.mensaje = "Pedido cancelado con exito"
            elif objeto["estatus"] == "Pagado":
                self.db.pedidos.update_one({"idPedido": idPedido},
                                           {"$set": {"estatus": "Devolucion", "motivoCancelacion": pedidoCancelacion.motivoCancelacion}})
                salida.estatus = "OK"
                salida.mensaje = "Se ha iniciado el proceso de reembolso"
            else:
                salida.estatus = "OK"
                salida.mensaje = "El pedido no existe o no se encuentran en Captura / Pagado"
        except Exception as ex:
            print(ex)
            salida.estatus = "ERROR"
            salida.mensaje = "El pedido no se puede cancelar, consulta al adminstrador."
        return salida

    def confirmarPedido(self, idPedido: str, pedidoConfirmacion: PedidoConfirmacion) -> Salida:
        salida = Salida(estatus="", mensaje="")
        try:
            pedido = self.db.pedidos.find_one({"_id": ObjectId(idPedido)})
            if not pedido:
                salida.estatus = "ERROR"
                salida.mensaje = f"Pedido con id {idPedido} no encontrado."
                return salida
            if pedido["estatus"] != "Pagado":
                salida.estatus = "ERROR"
                salida.mensaje = f"El pedido debe estar en estatus Pagado. Estatus actual: {pedido.get('estatus')}"
                return salida
            if 'detalle' not in pedido:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontró el detalle del pedido."
                return salida
            detalle_pedido = {item['idProducto']: item['cantidad'] for item in pedido['detalle']}
            for envioItem in pedidoConfirmacion.envio.detalle:
                if envioItem.idProducto not in detalle_pedido:
                    salida.estatus = "ERROR"
                    salida.mensaje = f"Producto con id {envioItem.idProducto} no encontrado en el pedido original."
                    return salida
                if envioItem.cantidad != detalle_pedido.get(envioItem.idProducto):
                    salida.estatus = "ERROR"
                    salida.mensaje = f"La cantidad enviada ({envioItem.cantidad}) para el producto {envioItem.idProducto} no coincide con la cantidad pedida ({detalle_pedido.get(envioItem.idProducto)})."
                    return salida
            update_data = {
                "$set": {
                    "fechaConfirmacion": datetime.now(),
                    "estatus": "Confirmado",
                    "envio": jsonable_encoder(pedidoConfirmacion.envio)
                }
            }
            result = self.db.pedidos.update_one({"_id": ObjectId(idPedido)}, update_data)
            if result.modified_count > 0:
                salida.estatus = "OK"
                salida.mensaje = f"Pedido con id: {idPedido} confirmado con éxito."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = f"No se pudo confirmar el pedido con id: {idPedido}. (Puede que ya estuviera confirmado o no se encontró)."
        except Exception as ex:
            print(f"Error al confirmar el pedido {idPedido}: {ex}")
            salida.estatus = "ERROR"
            salida.mensaje = "Error al confirmar el pedido, consulta al administrador."
        return salida

    def consultarPedidoPorID(self, idPedido: str) -> PedidosSalidaID:
        salida = PedidosSalidaID(estatus="", mensaje="", pedido=None)
        try:
            pedido_data = self.db.consultaIDView.find_one({"idPedido": idPedido})
            if pedido_data:
                salida.pedido = pedido_data
                salida.estatus = "OK"
                salida.mensaje = f"Pedido {idPedido} encontrado con extito."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = f"El pedido con id {idPedido} no se ha encontrado."
        except Exception as e:
                print(f"Error al consultar el pedido {idPedido}: {e}")
                salida.estatus = "ERROR"
                salida.mensaje = "Error interno al consultar el pedido."
        return salida

    def registrarTracking(self, idPedido: str, evento: RegistrarEvento) -> Salida:
        salida = Salida(estatus="", mensaje="")
        try:
            pedido = self.db.pedidos.find_one({"_id": ObjectId(idPedido)})
            if not pedido or pedido.get("estatus") != "Confirmado":
                salida.estatus = "ERROR"
                salida.mensaje = "El pedido no existe o no se encuentra en estado Confirmado"
                return salida
            if "envio" not in pedido:
                salida.estatus = "ERROR"
                salida.mensaje = "El pedido no contiene información de envío"
                return salida
            tracking_event = {
                "evento": evento.evento,
                "lugar": evento.lugar,
                "fecha": evento.fecha
            }
            update_result = self.db.pedidos.update_one(
                {"_id": ObjectId(idPedido)},
                {
                    "$push": {
                        "envio.tracking": tracking_event
                    }
                }
            )
            if update_result.modified_count > 0:
                salida.estatus = "OK"
                salida.mensaje = f"Evento de tracking registrado exitosamente en el pedido con id: {idPedido}"
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se pudo registrar el evento de tracking"
        except Exception as ex:
            print(f"Error al registrar tracking: {ex}")
            salida.estatus = "ERROR"
            salida.mensaje = "Error al registrar el evento de tracking, consulte al administrador"
        return salida

    def trackingPedido(self, idPedido: str):
        salida = PedidoEnvioSalida(estatus="", mensaje="", pedido=None)
        try:
            pedidoTracking = self.db.consultarHistorialView.find_one({"idPedido": idPedido})
            if pedidoTracking:
                salida.estatus = "OK"
                salida.mensaje = "Consulta de tracking exitosa"
                salida.pedido = pedidoTracking
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontró información de tracking para el pedido."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error interno al consultar el tracking del pedido"
        return salida