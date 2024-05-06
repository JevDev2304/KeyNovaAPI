from fastapi import APIRouter, status, HTTPException
from database_connection.dbConnection import ConnectionDB
from schemas.access import access_schema, accesses_schema
from models.access import Access
from fastapi.responses import JSONResponse


dbConnection = ConnectionDB()
accessRouter = APIRouter(prefix="/access", tags=["access"])

@accessRouter.get("/", response_model=list[Access])
async def accessses():
    accessses = accesses_schema(dbConnection.obtener_accesos())
    return JSONResponse(content=accessses)

@accessRouter.get("/{Propiedad_idPropiedad}/{Agente_idAgente}", response_model=Access)
async def access(Propiedad_idPropiedad : str, Agente_idAgente: str):
    access = dbConnection.obtener_accesos_por_id_agente(int(Propiedad_idPropiedad), int(Agente_idAgente))
    access_dict = access_schema(access)
    return JSONResponse(content=access_dict)

@accessRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Access)
async def access(access: access):
    access_dict = dict(access)
    dbConnection.agregar_acceso(**access_dict)
    access_response_dict = access_schema(dbConnection.obtener_accesos_por_id_agente(access.Propiedad_idPropiedad,access.Agente_idAgente))
    return JSONResponse(content=access_response_dict)

@accessRouter.delete("/{Propiedad_idPropiedad}/{Agente_idAgente}", status_code=status.HTTP_200_OK, response_model=Access)
async def access(Propiedad_idPropiedad: str, Agente_idAgente: str):
    access = dbConnection.obtener_accesos_por_id_agente(int(Propiedad_idPropiedad),int(Agente_idAgente))
    access_dict = access_schema(access)
    dbConnection.eliminar_acceso(access_dict["Propiedad_idPropiedad"],access_dict["Agente_idAgente"])
    return JSONResponse(content=access_dict)
