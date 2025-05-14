from pydantic import BaseModel, Field
from models.pedidosModel import Salida

class Login(BaseModel):
    email: str
    password: str

class Usuario(BaseModel):
    idUsuario: int = Field(alias="_id")
    nombre: str
    email: str
    password: str
    estatus: str
    telefono: str
    tipo: str
    domicilio: str

class UsuarioSalida(Salida):
    usuario: Usuario | None = None