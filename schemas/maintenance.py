def maintenance_schema(maintenance :tuple) -> dict:
    return {
        "idMantenimiento": maintenance[0],
        "Propiedad_idPropiedad": maintenance[1],
        "descripcion": maintenance[2],
        "fecha": maintenance[3],
        "Agente_idAgente": maintenance[4],

    }

def maintenances_schema(maintenances :list) -> list:
    return [maintenance_schema(maintenance) for maintenance in maintenances]