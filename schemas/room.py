
def room_schema(room) -> dict:
    return {"idHabitacion" : str(room[0]),
            "Propietario_cedula" : str(room[1]),
            "direccion" : str(room[2]),
            "tipo" : str(room[3]),
           }

def rooms_schema(rooms) -> list:
    return [room_schema(room) for room in rooms]

