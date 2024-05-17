from fastapi import APIRouter, status, HTTPException, UploadFile, File
from database_connection.dbConnection import ConnectionDB
from schemas.room import room_schema, rooms_schema
from models.room import Room
from fastapi.responses import JSONResponse
import os
from tools.uploadImage import upload_img,  ABSOLUTE_IMG_DIR , delete_image


dbConnection = ConnectionDB()
roomRouter = APIRouter(prefix="/room", tags=["room"])


@roomRouter.get("/{id}", response_model=Room)
async def room(id: str):
    room = dbConnection.obtener_habitacion_por_id(int(id))
    room_dict = room_schema(room)
    return JSONResponse(content=room_dict)

@roomRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Room)
async def room(Propiedad_idPropiedad: int,nombre : str , image: UploadFile =File(...)):
    img_dir = await upload_img(ABSOLUTE_IMG_DIR, image)
    dict_room ={"Propiedad_idPropiedad": Propiedad_idPropiedad, "nombre":nombre, "imagen":img_dir}
    last_room = room_schema(dbConnection.agregar_habitacion(**dict_room))
    return JSONResponse(content=last_room)



@roomRouter.delete("/{id}", status_code=status.HTTP_200_OK, response_model=room)
async def room(id: str):
    room = dbConnection.obtener_habitacion_por_id(int(id))
    room_dict = room_schema(room)
    dbConnection.eliminar_habitacion(room_dict["idHabitacion"])
    delete_image(ABSOLUTE_IMG_DIR+room_dict["imagen"])
    return JSONResponse(content=room_dict)

