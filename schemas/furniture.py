def furniture_schema(furniture) -> dict:
    return {"idMueble": str(furniture[0]),
            "Habitacion_idHabitacion" : str(furniture[1]),
            "estado": str(furniture[2]),
            "imagen": str(furniture[3]),
            "descripcion": str(furniture[4]),
            "nombre": str(furniture[5])
           }


def furnitures_schema(furnitures) -> list:
    return [furniture_schema(furniture) for furniture in furnitures]