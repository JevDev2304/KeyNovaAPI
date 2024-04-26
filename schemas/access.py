def access_schema(access) -> dict:
    return {"idAccess": str(access["idAccess"]),
            "Propiedad_idPropiedad": str(access["Propiedad_idPropiedad"]),
            "Agente_idAgente": str(access["Agente_idAgente"])
            }


def accesses_schema(accesses) -> list:
    return [access_schema(access) for access in accesses]
