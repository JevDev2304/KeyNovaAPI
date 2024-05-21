
def agent_schema_bool(agent) -> dict:
    return {"idAgente" : str(agent[0]),
            "tipo" : str(agent[1]),
            "nombre" : str(agent[2]),
            "correo" : str(agent[3]),
            "contrasennia": str(agent[4]),
            "imagen": str(agent[5]),
            "clave_temporal": agent[6],
            "tieneAcceso":  agent[7]
           }
def agents_schema_bool(agents) -> list:
    return [agent_schema_bool(agent) for agent in agents]


