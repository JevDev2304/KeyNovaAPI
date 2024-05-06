def access_schema(access) -> dict:
    return {"Propiedad_idPropiedad": str(access[0]),
            "Agente_idAgente": str(access[1])
            }


def accesses_schema(accesses) -> list:
    return [access_schema(access) for access in accesses]
