from fastapi import APIRouter, status, HTTPException
from starlette.responses import JSONResponse
from database_connection.dbConnection import ConnectionDB
from schemas.owner import owner_schema
from schemas.property import property_schema
from tools.jwt_auth_agent import create_jwt_token
from schemas.agent import agents_schema, agent_schema
from tools.sendMail import sendmail
from tools.createHTML import OTPHTML, inventoryHTML
from schemas.agent import agent_schema

dbConnection = ConnectionDB()
agentRouter = APIRouter(prefix="/agent", tags=["agent"])

@agentRouter.post("/login",  status_code=status.HTTP_200_OK )
async def login(mail: str, password : str):
    agent = dbConnection.obtener_agente_por_correo(mail)
    agent_dict = agent_schema(agent)
    if (agent_dict["correo"] == mail and agent_dict["contrasennia"] == password):
        return JSONResponse(content={"token" :create_jwt_token(agent_dict),
                                     "info" : agent_dict})
    elif(agent_dict["correo"] == mail and agent_dict["contrasennia"] != password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect password")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not found")




#TODO OTPHTML(num)
@agentRouter.post("/sendOTP", status_code=status.HTTP_200_OK)
async def sendOTP(id_agent: int):
    agent = agent_schema(dbConnection.obtener_agente_por_id(id_agent))
    num=temporal_password(id_agent)
    sendmail(agent["correo"],"OTP VALIDATION", OTPHTML(num))

@agentRouter.get("/maintenanceAgents")
async def maintenanceAgents():
    agents = dbConnection.obtener_agentes_mantenimiento()
    return JSONResponse(content=agents_schema(agents))


@agentRouter.post("/inkInventory")
async def inkInventory(id_agent: int, num: int, id_propiedad :int):
    if validate_temporal_password(id_agent, num):
        send_inventory_mail_owner(id_propiedad)
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect OTP PASSWORD")



def validate_temporal_password(id_agent :int, num: int):
    agent = dbConnection.obtener_agente_por_id(id_agent)
    dict_agent = agent_schema(agent)
    num_bd = dict_agent["clave_temporal"]
    if num == num_bd:
        return True
    return False
def temporal_password(id_agent : int ):
    num=dbConnection.crear_clave_temporal(id_agent)
    return JSONResponse(content={"num" : num})


#TODO JUANFER inventoryHTML(inventory)
def send_inventory_mail_owner(id_prop :int):
    property= dbConnection.obtener_propiedad_por_id(id_prop)
    property_dict = property_schema(property)
    inventory = dbConnection.obtener_inventario_por_id_propiedad(property_dict["idPropiedad"])
    owner = owner_schema(dbConnection.obtener_propietario_por_id(property_dict["Propietario_idPropietario"]))
    sendmail(owner["correo"], f" Dear {owner['nombre']}, the Inventory of {property_dict['direccion']} is completed", inventoryHTML(inventory))
    dictResponse = {"message": f"Mail sent to{owner['correo']}  :) "}
    return JSONResponse(content=dictResponse)