from fastapi import APIRouter, status, HTTPException
from database_connection.dbConnection import ConnectionDB
from schemas.room import room_schema, rooms_schema
from models.room import Room
from fastapi.responses import JSONResponse

dbConnection = ConnectionDB()
roomRouter = APIRouter(prefix="/room", tags=["room"])

@roomRouter.get("/", response_model=list[Room])
async def rooms():
     rooms = rooms_schema(dbConnection.obtener_habitaciones())
     return JSONResponse(content=rooms)

@roomRouter.get("/{id}", response_model=Room)
async def room(id: str):
    room = dbConnection.obtener_habitacion_por_id(int(id))
    room_dict = room_schema(room)
    return JSONResponse(content=room_dict)

@roomRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=room)
async def room(room: room):
    room_dict = dict(room)
    del room_dict["idHabitacion"]
    dbConnection.agregar_habitacion(**room_dict)
    return JSONResponse(content=room_dict)

@roomRouter.delete("/{id}", status_code=status.HTTP_200_OK, response_model=room)
async def room(id: str):
    room_tuple = dbConnection.obtener_habitacion_por_id(int(id))
    room_dict = room_schema(room_tuple)
    dbConnection.eliminar_arrendamiento(room_dict["idHabitacion"])
    return JSONResponse(content=room_dict)

