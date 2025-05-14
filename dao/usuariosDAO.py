from itertools import count
from models.usuariosModel import UsuarioSalida

class UsuarioDAO:
    def __init__(self, db):
        self.db = db

    def comprobarUsuario(self, idUsuario: int):
        respuesta = False
        try:
            usuario = self.db.usuarios.find_one({"_id": idUsuario, "estatus": "A"})
            if usuario:
                respuesta = True
        except:
            respuesta = False
        return respuesta

    def comprobarTarjeta(self, idUsuario: int, noTarjeta: str):
        count = 0
        try:
            count = self.db.usuarios.count_documents({"_id": idUsuario, "estatus": "A", "tarjetas.noTarjeta": noTarjeta})
        except Exception as ex:
            print(ex)
        return count

    def autenticar(self, email, password):
        respuesta = UsuarioSalida(estatus="", mensaje="", usuario=None)
        try:
            usuario = self.db.usuarios.find_one({"email": email, "password": password, "estatus": "A"},
                                                projection={"tarjetas": False})
            if usuario:
                respuesta.estatus = "OK"
                respuesta.mensaje = "Usuario autenticado con exito"
                respuesta.usuario = usuario
            else:
                respuesta.estatus = "ERROR"
                respuesta.mensaje = "Datos incorrectos"
        except Exception as ex:
            print(ex)
            respuesta.estatus = "ERROR"
            respuesta.mensaje = "Error interno al autenticar el usuario, consulta al administrador"
        return respuesta