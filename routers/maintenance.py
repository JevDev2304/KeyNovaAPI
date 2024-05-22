from fastapi import APIRouter, status, HTTPException
from starlette.responses import JSONResponse
from database_connection.dbConnection import ConnectionDB
from models.maintenance import Maintenance
from tools.sendMail import sendmail
from schemas.maintenance import maintenance_schema, maintenances_schema
from schemas.property import property_schema
from schemas.owner import owner_schema
from datetime import datetime
from tools.createHTML import maintenanceHTML

dbConnection = ConnectionDB()
maintenancesRouter = APIRouter(prefix="/maintenance", tags=["maintenance"])

@maintenancesRouter.get("/agentIdMaintenance", response_model=list[Maintenance])
async def maintenances_of_agent_maintenance(id: int):
    maintenances = maintenances_schema(dbConnection.obtener_mantenimientos_por_id_agente_mantenimiento(id))
    return JSONResponse(status_code=status.HTTP_200_OK, content=maintenances)

@maintenancesRouter.get("/agentIdCommercial", response_model=list[Maintenance])
async def maintenances_of_agent_commercial(id: int):
    maintenances = dbConnection.obtener_mantenimientos_por_id_agente_comercial(id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=maintenances_schema(maintenances))

# FIXME
@maintenancesRouter.post("/")
async def maintenance(maintenance: Maintenance):
    property=property_schema(dbConnection.obtener_propiedad_por_id(maintenance.Propiedad_idPropiedad))
    if not check_date(maintenance.fecha):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date")
    owner= owner_schema(dbConnection.obtener_propietario_por_id_propiedad(maintenance.Propiedad_idPropiedad))
    dict_maintenance = vars(maintenance)
    del dict_maintenance["idMantenimiento"]
    # TODO  maintenanceHTML
    dbConnection.agregar_mantenimiento(maintenance.Propiedad_idPropiedad, maintenance.descripcion, maintenance.fecha, maintenance.Agente_idAgente)
    sendmail(owner["correo"], f"Maintenance for {property['direccion']} has been completed",
             maintenanceHTML(dict_maintenance))
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Maintenance created"})
@maintenancesRouter.get("/propertyId")
async def maintenances_of_property(id: int):
    maintenances = dbConnection.obtener_mantenimientos_por_id_propiedad(id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=maintenances_schema(maintenances))

@maintenancesRouter.delete("/")
async def delete_maintenance(id: int):
    dbConnection.eliminar_mantenimiento(id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Maintenance deleted"})

def check_date(date: str) -> bool:
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False
