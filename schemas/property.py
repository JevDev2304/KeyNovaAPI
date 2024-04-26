def property_schema(property) -> dict:
    return {"idPropiedad" : str(property["idPropiedad"]),
            "Propietario_cedula" : str(property["Propietario_cedula"]),
            "direccion" : str(property["direccion"]),
            "tipo" : str(property["tipo"]),
           }
def properties_schema(properties) -> list:
    return [property_schema(property) for property in properties]

