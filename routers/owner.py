from fastapi import APIRouter, status, HTTPException
from database_connection.dbConnection import ConnectionDB
from schemas.owner import owner_schema, owners_schema
from models.owner import Owner
from models.email import Email
from tools.sendMail import sendmail
from fastapi.responses import JSONResponse

dbConnection = ConnectionDB()
ownerRouter = APIRouter(prefix="/owner", tags=["owner"])

@ownerRouter.get("/", response_model=list[Owner])
async def owners():
     owners = owners_schema(dbConnection.obtener_propietarios())
     return JSONResponse(content=owners)

@ownerRouter.get("/{mail}", response_model=Owner)
async def owner(mail: str):
    owner = dbConnection.obtener_propietario_por_correo(mail)
    owner_dict = owner_schema(owner)
    return JSONResponse(content=owner_dict)

@ownerRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Owner)
async def owner(owner: Owner):
    owner_dict = dict(owner)
    owner_dict["genero"] = correctGenre(owner_dict["genero"])
    del owner_dict["idPropietario"]
    dbConnection.agregar_propietario(**owner_dict)
    owner_dict = owner_schema(dbConnection.obtener_propietario_por_correo(owner.correo))
    return JSONResponse(content=owner_dict)

@ownerRouter.delete("/{mail}", status_code=status.HTTP_200_OK, response_model=Owner)
async def owner(mail: str):
    owner = dbConnection.obtener_propietario_por_correo(mail)
    owner_dict = owner_schema(owner)
    dbConnection.eliminar_propietario(owner_dict["idPropietario"])
    return JSONResponse(content=owner_dict)

@ownerRouter.post("/sendmail/{mail}", status_code=status.HTTP_200_OK)
async def owner(email: Email, mail:str):
    dbConnection.obtener_propietario_por_correo(mail)
    sendmail(mail, email.subject, email.body)
    dictResponse = {"message": "Mail sent :) "}
    return JSONResponse(content=dictResponse)


def correctGenre(word: str):
    word_lower = word.lower()
    if word_lower == "masculino" or word_lower == "femenino" or word_lower == "otro":
        return word_lower
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You can only post an owner with those genres(masculino,femenino or otro)")