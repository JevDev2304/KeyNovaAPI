from fastapi import APIRouter, status, HTTPException, UploadFile, File
from database_connection.dbConnection import ConnectionDB
from schemas.furniture import furniture_schema, furnitures_schema
from models.furniture import Furniture
from fastapi.responses import JSONResponse
from tools.uploadImage import upload_img, ABSOLUTE_IMG_DIR, delete_image

dbConnection = ConnectionDB()
furnitureRouter = APIRouter(prefix="/furniture", tags=["furniture"])


@furnitureRouter.get("/{id}", response_model=Furniture)
async def furniture(id: int):
    furniture = dbConnection.obtener_mueble_por_id(id)
    furniture_dict = furniture_schema(furniture)
    return JSONResponse(content=furniture_dict)


@furnitureRouter.get("/room_furnitures/{room_id}", response_model=list[Furniture])
async def property_furnitures(room_id: int):
    furnitures = furnitures_schema(dbConnection.obtener_muebles_por_id_habitacion(room_id))
    return JSONResponse(furnitures)


@furnitureRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Furniture)
async def furniture(Habitacion_idHabitacion: int, estado: str, nombre: str, descripcion=None,
                    image: UploadFile = File(...)):
    check_state(estado)
    img_dir = await upload_img(ABSOLUTE_IMG_DIR, image)
    dict_furniture = {"Habitacion_idHabitacion": Habitacion_idHabitacion, "estado": estado, "nombre": nombre,
                      "imagen": img_dir, "descripcion": descripcion}
    last_furniture = furniture_schema(dbConnection.agregar_mueble(**dict_furniture))
    return JSONResponse(content=last_furniture)


@furnitureRouter.put("/", status_code=status.HTTP_200_OK, response_model=Furniture)
async def update_image(id: int, image: UploadFile = File(...)):
    img_dir = await upload_img(ABSOLUTE_IMG_DIR, image)
    furniture = furniture_schema(dbConnection.obtener_mueble_por_id(id))
    delete_image(ABSOLUTE_IMG_DIR + furniture["imagen"])
    del furniture["Habitacion_idHabitacion"]
    furniture["imagen"] = img_dir
    dbConnection.actualizar_mueble(**furniture)
    return JSONResponse(content={"message" : "Imagen actualizada"})


@furnitureRouter.put("/update_string", status_code=status.HTTP_200_OK, response_model=Furniture)
async def update_strings(id: int, estado: str, nombre: str, descripcion: str):
    check_state(estado)
    furniture = furniture_schema(dbConnection.obtener_mueble_por_id(id))
    dbConnection.actualizar_mueble(furniture["idMueble"], estado, furniture["imagen"], descripcion, nombre)
    final_furniture = furniture_schema(
        (furniture["idMueble"], furniture["Habitacion_idHabitacion"], estado, furniture["imagen"], descripcion, nombre))
    return JSONResponse(content=final_furniture)


@furnitureRouter.delete("/{id}", status_code=status.HTTP_200_OK, response_model=Furniture)
async def furniture(id: int):
    furniture = furniture_schema(dbConnection.eliminar_mueble(id))
    delete_image(ABSOLUTE_IMG_DIR + furniture["imagen"])
    return JSONResponse(content=furniture)


def check_state(state: str):
    states = ["pesimo", "malo", "regular", "bueno", "excelente"]
    if state in states:
        return
    else:
        return HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                             detail="You cannot post a furniture with this state ,please only use these states( pesimo, malo , regular , bueno , excelente)  ")
