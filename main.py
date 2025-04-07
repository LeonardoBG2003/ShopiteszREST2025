#Importar la clase fastapi del framework#
import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient

from dao.database import Conexion
from routers import pedidosRouter, productosRouter, usuariosRouter

#Crear una instancia de la clase fastapi#
app=FastAPI()

app.include_router(pedidosRouter.router)
app.include_router(productosRouter.router)
app.include_router(usuariosRouter.router)
@app.get("/")
async def home():
    salida = {"mensaje": "Bienvenido a PEDIDOSREST"}
    return salida

@app.on_event("startup")
async def startup():
    print("Conectando con MongoDB")
    conexion = Conexion()
    app.conexion = conexion
    app.db = conexion.getDB()

@app.on_event("shutdown")
async def shutdown():
    print("Cerrando la conexion con MongoDB")
    app.conexion.cerrar()

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', reload=True)