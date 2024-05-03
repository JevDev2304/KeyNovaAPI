from fastapi import APIRouter, status, HTTPException
from database_connection.dbConnection import ConnectionDB
from schemas.furniture import furniture_schema, furnitures_schema
from models.furniture import Furniture
from models.email import Email
from tools.sendMail import sendmail
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
    if type(furniture) == tuple:
        furniture_dict = furniture_schema(furniture)
        return JSONResponse(content=furniture_dict)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="furniture does not found")

@furnitureRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Furniture)
async def furniture(furniture: Furniture):
    furnitures = furnitures_schema(dbConnection.obtener_muebles())
    isRepeated = repeatedImage(furniture, furnitures)
    if isRepeated:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Furniture with this image already exist")
    else:
        furniture_dict = dict(furniture)
        del furniture_dict["idMueble"]
        dbConnection.agregar_mueble(**furniture_dict)
        furniture_dict = furniture_schema(dbConnection.obtener_mueble_por_imagen(furniture.imagen))
        return JSONResponse(content=furniture_dict)

@furnitureRouter.delete("/{imagen}", status_code=status.HTTP_200_OK, response_model=furniture)
async def furniture(imagen: str):
    furniture = dbConnection.obtener_mueble_por_imagen(imagen)
    if type(furniture) == tuple:
        furniture_dict = furniture_schema(furniture)
        dbConnection.eliminar_mueble(furniture_dict["idMueble"])
        return JSONResponse(content=furniture_dict)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="furniture does not found")


def repeatedImage(furniture: Furniture, furnitures: list[dict]) -> bool:
    isRepeated: bool = False
    for furniture_i in furnitures:
        if furniture_i["imagen"] == furniture.imagen:
            isRepeated = True
    if isRepeated:
        return True
    else:
        return False
