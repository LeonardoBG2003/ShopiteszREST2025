from fastapi import APIRouter, Request, Depends
from dao.usuariosDAO import UsuarioDAO
from models.usuariosModel import Login, UsuarioSalida
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

security = HTTPBasic()

@router.post("/autenticar", response_model = UsuarioSalida, summary="Autenticar un usuario")
async def login(login: Login, request: Request) -> UsuarioSalida:
    usuarioDAO = UsuarioDAO(request.app.db)
    return usuarioDAO.autenticar(login.email, login.password)

async def validarUsuario(request: Request, credenciales: HTTPBasicCredentials = Depends(security)) -> UsuarioSalida:
    usuarioDAO = UsuarioDAO(request.app.db)
    return usuarioDAO.autenticar(credenciales.username, credenciales.password)