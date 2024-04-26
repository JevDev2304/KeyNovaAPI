
def room_schema(room) -> dict:
    return {"idHabitacion" : str(room["idHabitacion"]),
            "Propietario_cedula" : str(room["Propietario_cedula"]),
            "direccion" : str(room["direccion"]),
            "tipo" : str(room["tipo"]),
           }

def rooms_schema(rooms) -> list:
    return [room_schema(room) for room in rooms]

