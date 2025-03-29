from fastapi import APIRouter

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.get("/usuarios/login")
async def login():
    return {"mensaje": "Validando las credenciales del usuario"}
