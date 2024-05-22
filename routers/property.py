from fastapi import APIRouter, status, HTTPException, UploadFile, File
from database_connection.dbConnection import ConnectionDB
from schemas.property import property_schema, properties_schema
from schemas.owner import owner_schema
from models.property import Property
from fastapi.responses import JSONResponse
from tools.sendMail import sendmail
from tools.uploadImage import upload_img, ABSOLUTE_IMG_DIR , delete_image
from tools.createHTML import inventoryHTML

dbConnection = ConnectionDB()
propertyRouter = APIRouter(prefix="/property", tags=["property"])
@propertyRouter.get("/", response_model=Property)
async def property(id: str):
    property = dbConnection.obtener_propiedad_por_id(int(id))
    property_dict = property_schema(property)
    return JSONResponse(content=property_dict)

@propertyRouter.get("/ownerProperties", response_model=list[Property])
async def owner_properties(owner_id: str):
    properties = dbConnection.obtener_propiedades_por_id_propietario(int(owner_id))
    properties = properties_schema(properties)
    return JSONResponse(content=properties)
@propertyRouter.get("/agentProperties", response_model=list[Property])
async def agent_properties(agent_id: str):
    properties = dbConnection.obtener_propiedades_por_id_agente(int(agent_id))
    properties = properties_schema(properties)
    return JSONResponse(content=properties)





@propertyRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Property)
async def property(idAgente, Propietario_idPropietario: int, direccion: str, image: UploadFile = File(...)):
    img_dir = await upload_img(ABSOLUTE_IMG_DIR, image)
    dict_property = {
        "Propietario_idPropietario": Propietario_idPropietario,
        "direccion": direccion,
        "imagen": img_dir,
        "firmado": 0}
    last_property = property_schema(dbConnection.agregar_propiedad_con_agente(idAgente, **dict_property))
    return JSONResponse(content=last_property)



@propertyRouter.delete("/{id}", status_code=status.HTTP_200_OK, response_model=Property)
async def property(id: str):
    property = dbConnection.obtener_propiedad_por_id(int(id))
    property_dict = property_schema(property)
    dbConnection.eliminar_propiedad(property_dict["idPropiedad"])
    delete_image(ABSOLUTE_IMG_DIR + property_dict["imagen"])
    return JSONResponse(content=property_dict)

