from fastapi import APIRouter, status, HTTPException
from database_connection.dbConnection import ConnectionDB
from schemas.property import property_schema, properties_schema
from models.property import Property
from fastapi.responses import JSONResponse

dbConnection = ConnectionDB()
propertyRouter = APIRouter(prefix="/property", tags=["property"])



@propertyRouter.get("/{id}", response_model=Property)
async def property(id: str):
    property = dbConnection.obtener_propiedad_por_id(int(id))
    property_dict = property_schema(property)
    return JSONResponse(content=property_dict)

@propertyRouter.get("/", response_model=list[Property])
async def owner_properties(owner_id: str):
    properties = dbConnection.obtener_propiedades_por_id_propietario(int(owner_id))
    properties = properties_schema(properties)
    return JSONResponse(content=properties)



@propertyRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Property)
async def property(property: Property):
    property_dict = vars(property)
    del property_dict["idPropiedad"]
    print(property_dict)
    last_property = property_schema(dbConnection.agregar_propiedad(**property_dict))
    return JSONResponse(content=last_property)


@propertyRouter.delete("/{id}", status_code=status.HTTP_200_OK, response_model=Property)
async def property(id: str):
    property = dbConnection.obtener_propiedad_por_id(int(id))
    property_dict = property_schema(property)
    dbConnection.eliminar_propiedad(property_dict["idPropiedad"])
    return JSONResponse(content=property_dict)

