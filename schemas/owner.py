
def owner_schema(owner) -> dict:
    return {"idPropietario" : int(owner[0]),
            "nombre" : str(owner[1]),
            "correo" : str(owner[2]),
            "genero": str(owner[3]),
            "contrassenia": str(owner[4]),
            "agente_idAgente": int (owner[5]),
            "cedula" : str(owner[6]),
            "celular": str(owner[7])
           }
def owners_schema(owners) -> list:
    return [owner_schema(owner) for owner in owners]

