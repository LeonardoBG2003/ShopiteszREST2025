from fastapi import APIRouter, Request
from dao.usuariosDAO import UsuarioDAO
from models.usuariosModel import Login, UsuarioSalida

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post("/autenticar", response_model = UsuarioSalida, summary="Autenticar un usuario")
async def login(login: Login, request: Request) -> UsuarioSalida:
    usuarioDAO = UsuarioDAO(request.app.db)
    return usuarioDAO.autenticar(login.email, login.password)
