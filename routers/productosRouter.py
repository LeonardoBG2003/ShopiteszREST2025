from fastapi import APIRouter, Request
from typing import Any
from dao.productosDAO import ProductoDAO
from models.productosModel import ProductosSalida

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

@router.get("/", response_model = ProductosSalida)
async def consultaGeneral(request: Request)->Any:
    #return {"mensaje": "Consultando los productos"}
    productoDAO = ProductoDAO(request.app.db)
    return productoDAO.consultaGeneral()

@router.get("/{idProducto}")
async def consultaIndividual(idProducto:int):
    return {"mensaje": "Consultando el producto con id: "+ str(idProducto)}

@router.get("/vendedor/{idVendedor}")
async def consultarPorVendedor(idVendedor:str):
    return {"mensaje": "Consultando productos del vendedor: "+ idVendedor}

@router.get("/categoria/{idCategoria}")
async def consultarPorCategoria(idCategoria:int):
    return {"mensaje": "Consultando productos de la categoria: "+ str(idCategoria)}
