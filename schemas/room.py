
def room_schema(room) -> dict:
    return {"idHabitacion" : int(room[0]),
            "Propiedad_idPropiedad" : int(room[1]),
            "imagen" : str(room[2]),
            "nombre": str(room[3]),
            "descripcion" : str(room[4])
           }

def rooms_schema(rooms) -> list:
    return [room_schema(room) for room in rooms]

