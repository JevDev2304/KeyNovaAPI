from fastapi import APIRouter, status, HTTPException
from database_connection.dbConnection import ConnectionDB
from schemas.tenant import tenant_schema, tenants_schema
from models.tenant import Tenant
from models.email import Email
from tools.sendMail import sendmail
from fastapi.responses import JSONResponse

dbConnection = ConnectionDB()
tenantRouter = APIRouter(prefix="/tenant", tags=["tenant"])

@tenantRouter.get("/", response_model=list[Tenant])
async def tenants():
     tenants = tenants_schema(dbConnection.obtener_arrendatarios())
     return JSONResponse(content=tenants)

@tenantRouter.get("/{mail}", response_model=Tenant)
async def tenant(mail: str):
    tenant = dbConnection.obtener_arrendatario_por_correo(mail)
    tenant_dict = tenant_schema(tenant)
    return JSONResponse(content=tenant_dict)

@tenantRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Tenant)
async def tenant(tenant: Tenant):
    tenant_dict = dict(tenant)
    correctGenre(tenant_dict["genero"])
    del tenant_dict["idArrendatario"]
    dbConnection.agregar_arrendatario(**tenant_dict)
    tenant_dict = tenant_schema(dbConnection.obtener_arrendatario_por_correo(tenant.correo))
    return JSONResponse(content=tenant_dict)

@tenantRouter.delete("/{mail}", status_code=status.HTTP_200_OK, response_model=Tenant)
async def tenant(mail: str):
    tenant = dbConnection.obtener_arrendatario_por_correo(mail)
    tenant_dict = tenant_schema(tenant)
    dbConnection.eliminar_arrendatario(tenant_dict["idArrendatario"])
    return JSONResponse(content=tenant_dict)

@tenantRouter.post("/sendmail/{mail}", status_code=status.HTTP_200_OK)
async def owner(email: Email, mail:str):
    dbConnection.obtener_arrendatario_por_correo(mail)
    sendmail(mail, email.subject, email.body)
    dictResponse = {"message": "Mail sent :) "}
    return JSONResponse(content=dictResponse)

def correctGenre(word: str):
    word_lower = word.lower()
    if word_lower == "masculino" or word_lower == "femenino" or word_lower == "otro":
        return word_lower
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You can only post a tenant with those genres(masculino,femenino or otro)")