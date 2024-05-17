
def agent_schema(agent) -> dict:
    return {"idAgente" : str(agent[0]),
            "tipo" : str(agent[1]),
            "nombre" : str(agent[2]),
            "correo" : str(agent[3]),
            "contrasennia": str(agent[4]),
            "imagen": str(agent[5]),
            "clave_temporal": agent[6]
           }
def agents_schema(agents) -> list:
    return [agent_schema(agent) for agent in agents]


