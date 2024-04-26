
def owner_schema(owner) -> dict:
    return {"idPropietario" : str(owner[0]),
            "nombre" : str(owner[1]),
            "correo" : str(owner[2]),
            "edad" : str(owner[3]),
            "genero": str(owner[4])
           }
def owners_schema(owners) -> list:
    return [owner_schema(owner) for owner in owners]

