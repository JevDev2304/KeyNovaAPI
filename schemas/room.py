
def room_schema(room) -> dict:
    return {"idHabitacion" : str(room[0]),
            "Propiedad_idPropiedad" : str(room[1]),
            "estado" : str(room[2]),
            "video" : str(room[3]),
            "nombre": str(room[4])
           }

def rooms_schema(rooms) -> list:
    return [room_schema(room) for room in rooms]

