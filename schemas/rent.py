def rent_schema(rent) -> dict:
    return {"idArrendamiento" : str(rent["idArrendamiento"]),
            "Propiedad_idPropiedad" : str(rent["Propiedad_idPropiedad"]),
            "Arrendatario_idArrendatario" : str(rent["Arrendatario_idArrendatario"]),
            "fecha_inicio" : str(rent["fecha_inicio"]),
            "fecha_final": str(rent["fecha_final"])
           }
def rents_schema(rents) -> list:
    return [rent_schema(rent) for rent in rents]

