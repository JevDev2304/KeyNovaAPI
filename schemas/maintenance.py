def maintenance_schema(maintenance :tuple) -> dict:
    return {
        "idMantenimiento": maintenance[0],
        "Propiedad_idPropiedad": maintenance[1],
        "estado": maintenance[2],
        "imagen": maintenance[3],
        "descripcion": maintenance[4]
    }

def maintenances_schema(maintenances :list) -> list:
    return [maintenance_schema(maintenance) for maintenance in maintenances]