
def tenant_schema(tenant) -> dict:
    return {"idArrendatario" : str(tenant["idArrendatario"]),
            "nombre" : str(tenant["nombre"]),
            "correo" : str(tenant["correo"]),
            "edad" : str(tenant["edad"]),
            "genero": str(tenant["genero"])
           }

def tenants_schema(tenants) -> list:
    return [tenant_schema(tenant) for tenant in tenants]

