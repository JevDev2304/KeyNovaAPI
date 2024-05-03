
def agent_schema(agent) -> dict:
    return {"idAgente" : str(agent[0]),
            "nombre" : str(agent[1]),
            "correo" : str(agent[2]),
            "contrasennia" : str(agent[3]),
            "tipo": str(agent[4])
           }
def agents_schema(agents) -> list:
    return [agent_schema(agent) for agent in agents]


