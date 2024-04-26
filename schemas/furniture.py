def furniture_schema(furniture) -> dict:
    return {"idMueble": str(furniture["idMueble"]),
            "Habitacion_idHabitacion" : str(furniture["Habitacion_idHabitacion"]),
            "estado": str(furniture["estado"]),
            "imagen": str(furniture["imagen"]),
            "descripcion": str(furniture["descripcion"])
           }


def furnitures_schema(furnitures) -> list:
    return [furniture_schema(furniture) for furniture in furnitures]