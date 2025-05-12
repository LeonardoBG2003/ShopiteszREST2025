from pydantic import BaseModel
from models.pedidosModel import Vendedor, Salida

class Categoria(BaseModel):
    idCategoria: int
    nombre: str

class Producto(BaseModel):
    idProducto: int
    nombre: str
    descripcion: str
    precio: float
    costoEnvio : float
    existencia : int
    color : str
    marca : str
    estatus: str
    categoria: Categoria
    vendedor: Vendedor

class ProductosSalida(Salida):
    productos : list[Producto]