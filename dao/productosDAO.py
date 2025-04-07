from models.productosModel import ProductosSalida

class ProductoDAO:
    def __init__(self, db):
        self.db = db

    def consultaGeneral(self):
        salida = ProductosSalida(estatus = "", mensaje = "", productos = [])
        try:
            lista = list(self.db.productosView.find())
            salida.estatus = "OK"
            salida.mensaje = "Listado de productos"
            salida.productos = lista
        except:
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar los productos."
            salida.productos = None
        return salida
