from fastapi import APIRouter, status, HTTPException
from database_connection.dbConnection import ConnectionDB
from schemas.owner import owner_schema, owners_schema
from models.owner import Owner
from tools.sendMail import sendmail
from tools.createHTML import inventoryHTML
from fastapi.responses import JSONResponse

dbConnection = ConnectionDB()
ownerRouter = APIRouter(prefix="/owner", tags=["owner"])



@ownerRouter.get("/{mail}", response_model=Owner)
async def owner(mail: str):
    owner = dbConnection.obtener_propietario_por_correo(mail)
    owner_dict = owner_schema(owner)
    return JSONResponse(content=owner_dict)

@ownerRouter.get("/owners_of_agent/{id}", response_model=list[Owner])
async def owners_of_agent(idProperty: str):
    owners = dbConnection.obtener_propietarios_por_id_agente(int(idProperty))
    owners_list = owners_schema(owners)
    return JSONResponse(content=owners_list)

@ownerRouter.get("/ownerOfProperty/{idProperty}", response_model=Owner)
async def owner(idProperty: int):
    owner = dbConnection.obtener_propietario_por_id_propiedad(int(idProperty))
    owner_dict = owner_schema(owner)
    return JSONResponse(content=owner_dict)

@ownerRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Owner)
async def owner(owner: Owner):
    owner_dict = dict(owner)
    owner_dict["genero"] = correctGenre(owner_dict["genero"])
    del owner_dict["idPropietario"]
    owner_dict = owner_schema(dbConnection.agregar_propietario(**owner_dict))
    return JSONResponse(content=owner_dict)




# FIXME METODO EN BD PARA BORRAR PROPIETARIO POR CORREO
@ownerRouter.delete("/{mail}", status_code=status.HTTP_200_OK, response_model=Owner)
async def owner(mail: str):
    owner = dbConnection.obtener_propietario_por_correo(mail)
    owner_dict = owner_schema(owner)
    dbConnection.eliminar_propietario(owner_dict["idPropietario"])
    return JSONResponse(content=owner_dict)

@ownerRouter.post("/sendInventory/{property_id}", status_code=status.HTTP_200_OK)
async def owner(property_id: int):
    owner = owner_schema(dbConnection.obtener_propietario_por_id_propiedad(property_id))
    inventory = dbConnection.obtener_inventario_por_id_propiedad(property_id)
    sendmail(owner["correo"], f"Dear {owner['nombre']}, here is your new inventory",inventoryHTML(inventory))
    dictResponse = {"message": "Mail sent :) "}
    return JSONResponse(content=dictResponse)



def correctGenre(word: str):
    word_lower = word.lower()
    if word_lower == "masculino" or word_lower == "femenino" or word_lower == "otro":
        return word_lower
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You can only post an owner with those genres(masculino,femenino or otro)")