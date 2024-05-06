from fastapi import APIRouter, status, HTTPException
from database_connection.dbConnection import ConnectionDB
from schemas.property import property_schema, properties_schema
from models.property import Property
from fastapi.responses import JSONResponse

dbConnection = ConnectionDB()
propertyRouter = APIRouter(prefix="/property", tags=["property"])


@propertyRouter.get("/", response_model=list[Property])
async def properties():
    properties = properties_schema(dbConnection.obtener_propiedades())
    return JSONResponse(content=properties)


@propertyRouter.get("/{id}", response_model=Property)
async def property(id: str):
    property = dbConnection.obtener_propiedad_por_id(id)
    property_dict = property_schema(property)
    return JSONResponse(content=property_dict)



@propertyRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Property)
async def property(property: property):
    property_dict = dict(property)
    del property_dict["idPropiedad"]
    dbConnection.agregar_propiedad(**property_dict)
    property_dict = property_schema(dbConnection.obtener_propiedad_por_direccion(property.direccion))
    return JSONResponse(content=property_dict)


@propertyRouter.delete("/{id}", status_code=status.HTTP_200_OK, response_model=Property)
async def property(id: str):
    property = dbConnection.obtener_propiedad_por_id(id)
    property_dict = property_schema(property)
    dbConnection.eliminar_propiedad(property_dict["idPropiedad"])
    return JSONResponse(content=property_dict)

