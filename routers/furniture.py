from fastapi import APIRouter, status, HTTPException
from database_connection.dbConnection import ConnectionDB
from schemas.furniture import furniture_schema, furnitures_schema
from models.furniture import Furniture
from fastapi.responses import JSONResponse


dbConnection = ConnectionDB()
furnitureRouter = APIRouter(prefix="/furniture", tags=["furniture"])

@furnitureRouter.get("/", response_model=list[Furniture])
async def furnitures():
    furnitures = furnitures_schema(dbConnection.obtener_muebles())
    return JSONResponse(content=furnitures)

@furnitureRouter.get("/{id}", response_model=Furniture)
async def furniture(id: str):
    furniture = dbConnection.obtener_mueble_por_id(id)
    furniture_dict = furniture_schema(furniture)
    return JSONResponse(content=furniture_dict)

@furnitureRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Furniture)
async def furniture(furniture: Furniture):
    furniture_dict = dict(furniture)
    del furniture_dict["idMueble"]
    dbConnection.agregar_mueble(**furniture_dict)
    furniture_response_dict = furniture_schema(dbConnection.obtener_mueble_por_imagen(furniture.imagen))
    return JSONResponse(content=furniture_response_dict)

@furnitureRouter.delete("/{imagen}", status_code=status.HTTP_200_OK, response_model=furniture)
async def furniture(imagen: str):
    furniture = dbConnection.obtener_mueble_por_imagen(imagen)
    furniture_dict = furniture_schema(furniture)
    dbConnection.eliminar_mueble(furniture_dict["idMueble"])
    return JSONResponse(content=furniture_dict)
