from itertools import count


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