def rent_schema(rent) -> dict:
    return {"idArrendamiento" : str(rent[0]),
            "Propiedad_idPropiedad" : str(rent[1]),
            "Arrendatario_idArrendatario" : str(rent[2]),
            "fecha_inicio" : str(rent[3]),
            "fecha_final": str(rent[4])
           }
def rents_schema(rents) -> list:
    return [rent_schema(rent) for rent in rents]

