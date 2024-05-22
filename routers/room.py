from fastapi import APIRouter, status, HTTPException, UploadFile, File
from database_connection.dbConnection import ConnectionDB
from schemas.room import room_schema, rooms_schema
from models.room import Room
from fastapi.responses import JSONResponse
from tools.uploadImage import upload_img,  ABSOLUTE_IMG_DIR , delete_image


dbConnection = ConnectionDB()
roomRouter = APIRouter(prefix="/room", tags=["room"])


@roomRouter.get("/{id}", response_model=Room)
async def room(id: int):
    room = dbConnection.obtener_habitacion_por_id(id)
    room_dict = room_schema(room)
    return JSONResponse(content=room_dict)

@roomRouter.get("/property_rooms/{property_id}", response_model=list[Room])
async def property_rooms(property_id:int):
    rooms = rooms_schema(dbConnection.obtener_habitaciones_por_id_propiedad(property_id))
    return JSONResponse(rooms)


@roomRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Room)
async def room(Propiedad_idPropiedad: int,nombre : str , descripcion = None, image: UploadFile =File(...)):
    img_dir = await upload_img(ABSOLUTE_IMG_DIR, image)
    dict_room ={"Propiedad_idPropiedad": Propiedad_idPropiedad, "nombre":nombre, "imagen":img_dir, "descripcion" : descripcion}
    last_room = room_schema(dbConnection.agregar_habitacion(**dict_room))
    return JSONResponse(content=last_room)
@roomRouter.put("/", status_code=status.HTTP_200_OK, response_model=Room)
async def update_image(id:int , image: UploadFile = File(...)):
    img_dir = await upload_img(ABSOLUTE_IMG_DIR, image)
    room_dict = room_schema(dbConnection.obtener_habitacion_por_id(id))
    room = room_dict.copy()
    delete_image(ABSOLUTE_IMG_DIR + room["imagen"])
    del room["Propiedad_idPropiedad"]
    room["imagen"] = img_dir
    dbConnection.actualizar_habitacion(**room)
    room_final = room_schema((room_dict["idHabitacion"],room_dict["Propiedad_idPropiedad"],img_dir,room_dict["nombre"],room_dict["descripcion"]))
    return JSONResponse(content=room_final)


@roomRouter.put("/update_string", status_code=status.HTTP_200_OK,response_model=Room)
async def update_strings(id:int ,nombre :str, descripcion : str):
    room = room_schema(dbConnection.obtener_habitacion_por_id(id))
    dbConnection.actualizar_habitacion(room["idHabitacion"], room["imagen"], nombre, descripcion)
    final_room = room_schema((room["idHabitacion"],room["Propiedad_idPropiedad"],room["imagen"],nombre,descripcion))
    return JSONResponse(content=final_room)




@roomRouter.delete("/{id}", status_code=status.HTTP_200_OK, response_model=Room)
async def room(id: int):
    room = room_schema(dbConnection.eliminar_habitacion(id))
    delete_image(ABSOLUTE_IMG_DIR+room["imagen"])
    return JSONResponse(content=room)


