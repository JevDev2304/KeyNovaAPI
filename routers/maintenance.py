from fastapi import APIRouter, status, HTTPException
from starlette.responses import JSONResponse
from database_connection.dbConnection import ConnectionDB
from models.maintenance import Maintenance
from schemas.maintenance import maintenance_schema, maintenances_schema

dbConnection = ConnectionDB()
maintenancesRouter = APIRouter(prefix="/maintenance", tags=["maintenance"])

@maintenancesRouter.get("/", response_model=list[Maintenance])
async def maintenances_of_agent(id: int):
    if dbConnection.existe_agente_con_id(id):
        maintenances = dbConnection.obtener_mantenimientos_por_id_agente(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=maintenances_schema(maintenances))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this id was not found")