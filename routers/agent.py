from fastapi import APIRouter, status, HTTPException
from starlette.responses import JSONResponse
from database_connection.dbConnection import ConnectionDB
from models.agent import Agent
from schemas.agent import agent_schema,agents_schema

dbConnection = ConnectionDB()
agentRouter = APIRouter(prefix="/agent", tags=["agent"])

@agentRouter.get("/{mail}/{password}",  status_code=status.HTTP_200_OK)
async def login(mail: str, password : str):
    agent = dbConnection.obtener_agente_por_correo(mail)
    if type(agent) == tuple:
        agent_dict = agent_schema(agent)
        if (agent_dict["correo"] == mail and agent_dict["contrasennia"] == password):
            return JSONResponse(content={"message": "The mail and password are correct :) "})
        elif(agent_dict["correo"] == mail and agent_dict["contrasennia"] != password):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect password")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not found")
