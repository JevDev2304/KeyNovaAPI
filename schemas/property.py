def property_schema(property) -> dict:
    return {"idPropiedad" : int(property[0]),
            "Propietario_idPropietario" : int(property[1]),
            "direccion" : str(property[2]),
            "imagen" : str(property[3]),
            "firmado": int(property[4])}

def properties_schema(properties) -> list:
    return [property_schema(property) for property in properties]

