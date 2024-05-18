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
    if dbConnection.existe_agente_con_id(id):
        maintenances = dbConnection.obtener_mantenimientos_por_id_agente_mantenimiento(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=maintenances_schema(maintenances))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance Agent with this id was not found")

@maintenancesRouter.get("/agentIdCommercial", response_model=list[Maintenance])
async def maintenances_of_agent_commercial(id: int):
    if dbConnection.existe_agente_con_id(id):
        maintenances = dbConnection.obtener_mantenimientos_por_id_agente_comercial(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=maintenances_schema(maintenances))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comercial Agent with this id was not found")
@maintenancesRouter.post("/")
async def maintenance(maintenance: Maintenance):
    property=property_schema(dbConnection.obtener_propiedad_por_id(maintenance.Propiedad_idPropiedad))
    dbConnection.obtener_agente_por_id(maintenance.Agente_idAgente)
    if not check_date(maintenance.fecha):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date")
    #TODO obtener_propietario_por_id_propiedad
    owner= owner_schema(dbConnection.obtener_propietario_por_id_propiedad(maintenance.Propiedad_idPropiedad))
    dict_maintenance = vars(maintenance)
    del dict_maintenance["idMantenimiento"]
    # TODO  maintenanceHTML
    sendmail(owner["correo"],f"Maintenance for {property['direccion']} has been completed", maintenanceHTML(dict_maintenance))
    dbConnection.agregar_mantenimiento(maintenance.Propiedad_idPropiedad, maintenance.descripcion, maintenance.fecha, maintenance.Agente_idAgente)

@maintenancesRouter.get("/propertyId")
async def maintenances_of_property(id: int):
    if dbConnection.existe_propiedad_con_id(id):
        maintenances = dbConnection.obtener_mantenimientos_por_id_propiedad(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=maintenances_schema(maintenances))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property with this id was not found")

@maintenancesRouter.delete("/")
async def delete_maintenance(id: int):
    if dbConnection.existe_mantenimiento_con_id(id):
        dbConnection.eliminar_mantenimiento(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Maintenance deleted"})
def check_date(date: str) -> bool:
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False
