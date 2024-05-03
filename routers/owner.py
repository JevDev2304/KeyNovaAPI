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
    if type(owner) == tuple:
        owner_dict = owner_schema(owner)
        return JSONResponse(content=owner_dict)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner does not found")

@ownerRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Owner)
async def owner(owner: Owner):
    owners = owners_schema(dbConnection.obtener_propietarios())
    isRepeated = repeatedMail(owner, owners)
    if isRepeated:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="The owner mail already exist")
    else:
        owner_dict = dict(owner)
        del owner_dict["idPropietario"]
        dbConnection.agregar_propietario(**owner_dict)
        owner_dict = owner_schema(dbConnection.obtener_propietario_por_correo(owner.correo))
        return JSONResponse(content=owner_dict)

@ownerRouter.delete("/{mail}", status_code=status.HTTP_200_OK, response_model=Owner)
async def owner(mail: str):
    owner = dbConnection.obtener_propietario_por_correo(mail)
    if type(owner) == tuple:
        owner_dict = owner_schema(owner)
        dbConnection.eliminar_propietario(owner_dict["idPropietario"])
        return JSONResponse(content=owner_dict)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner does not found")

@ownerRouter.post("/sendmail/{mail}", status_code=status.HTTP_200_OK)
async def owner(email: Email, mail:str):
    owner = dbConnection.obtener_propietario_por_correo(mail)
    if isinstance(owner, tuple):
        sendmail(mail, email.subject, email.body)
        dictResponse = {"message": "Mail sent :) "}
        return JSONResponse(content=dictResponse)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this email does not found")

def repeatedMail(owner: Owner, owners: list[dict]) -> bool:
    isRepeated: bool = False
    for owner_i in owners:
        if owner_i["correo"] == owner.correo:
            isRepeated = True
    if isRepeated:
        return True
    else:
        return False
