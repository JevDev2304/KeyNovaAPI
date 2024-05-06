def property_schema(property) -> dict:
    return {"idPropiedad" : str(property[0]),
            "Propietario_idPropietario" : str(property[1]),
            "direccion" : str(property[2]),
            "tipo" : str(property[3]),
            "imagen" : str(property[4])
           }
def properties_schema(properties) -> list:
    return [property_schema(property) for property in properties]

