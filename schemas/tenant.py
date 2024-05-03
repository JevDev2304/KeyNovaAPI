
def tenant_schema(tenant) -> dict:
    return {"idArrendatario" : str(tenant[0]),
            "nombre" : str(tenant[1]),
            "correo" : str(tenant[2]),
            "edad" : str(tenant[3]),
            "genero": str(tenant[4])
           }

def tenants_schema(tenants) -> list:
    return [tenant_schema(tenant) for tenant in tenants]

