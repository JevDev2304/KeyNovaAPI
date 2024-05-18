from fastapi import APIRouter, status, HTTPException
from starlette.responses import JSONResponse
from database_connection.dbConnection import ConnectionDB
from tools.jwt_auth_agent import create_jwt_token
from schemas.agent import agent_schema

dbConnection = ConnectionDB()
agentRouter = APIRouter(prefix="/agent", tags=["agent"])

@agentRouter.post("/login",  status_code=status.HTTP_200_OK )
async def login(mail: str, password : str):
    agent = dbConnection.obtener_agente_por_correo(mail)
    agent_dict = agent_schema(agent)
    if (agent_dict["correo"] == mail and agent_dict["contrasennia"] == password):
        return JSONResponse(content={"token" :create_jwt_token(agent_dict),
                                     "info" : agent_dict})
    elif(agent_dict["correo"] == mail and agent_dict["contrasennia"] != password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect password")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not found")
