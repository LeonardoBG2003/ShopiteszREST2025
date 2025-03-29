from fastapi import APIRouter

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

@router.get("/")
async def consultaProductos():
    return {"mensaje": "Consultando los productos"}

@router.get("/{idProducto}")
async def consultarProducto(idProducto:int):
    return {"mensaje": "Consultando el producto: "+ str(idProducto)}

@router.get("/vendedor/{idVendedor}")
async def consultarPorVendedor(idVendedor:str):
    return {"mensaje": "Consultando productos del vendedor: "+ idVendedor}

@router.get("/categoria/{idCategoria}")
async def consultarPorCategoria(idCategoria:int):
    return {"mensaje": "Consultando productos de la categoria: "+ str(idCategoria)}
