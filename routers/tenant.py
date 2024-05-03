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
    if type(tenant) == tuple:
        tenant_dict = tenant_schema(tenant)
        return JSONResponse(content=tenant_dict)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found with the given email address.")

@tenantRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Tenant)
async def owner(tenant: Tenant):
    tenants = tenants_schema(dbConnection.obtener_arrendatarios())
    isRepeated = repeatedMail(tenant,tenants)
    if isRepeated:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="The tenant mail already exist")
    else:
        tenant_dict = dict(tenant)
        del tenant_dict["idArrendatario"]
        dbConnection.agregar_arrendatario(**tenant_dict)
        tenant_dict = tenant_schema(dbConnection.obtener_arrendatario_por_correo(tenant.correo))
        return JSONResponse(content=tenant_dict)

@tenantRouter.delete("/{mail}", status_code=status.HTTP_200_OK, response_model=Tenant)
async def tenant(mail: str):
    tenant = dbConnection.obtener_arrendatario_por_correo(mail)
    if type(tenant) == tuple:
        tenant_dict = tenant_schema(tenant)
        dbConnection.eliminar_arrendatario(tenant_dict["idArrendatario"])
        return JSONResponse(content=tenant_dict)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found with the given email address.")

@tenantRouter.post("/sendmail/{mail}", status_code=status.HTTP_200_OK)
async def owner(email: Email, mail:str):
    tenant = dbConnection.obtener_arrendatario_por_correo(mail)
    if isinstance(tenant, tuple):
        sendmail(mail, email.subject, email.body)
        dictResponse = {"message": "Mail sent :) "}
        return JSONResponse(content=dictResponse)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found with the given email address.")

def repeatedMail(tenant: Tenant, tenants: list[dict]) -> bool:
    isRepeated: bool = False
    for tenant_i in tenants:
        if tenant_i["correo"] == tenant.correo:
            isRepeated = True
    if isRepeated:
        return True
    else:
        return False
