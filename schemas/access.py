def access_schema(access) -> dict:
    return {"Propiedad_idPropiedad": int(access[0]),
            "Agente_idAgente": int(access[1])
            }


def accesses_schema(accesses) -> list:
    return [access_schema(access) for access in accesses]
