from fastapi import APIRouter, status, HTTPException
from database_connection.dbConnection import ConnectionDB
from schemas.rent import rent_schema, rents_schema
from models.rent import Rent
from fastapi.responses import JSONResponse

dbConnection = ConnectionDB()
rentRouter = APIRouter(prefix="/rent", tags=["rent"])

@rentRouter.get("/", response_model=list[Rent])
async def rents():
     rents = rents_schema(dbConnection.obtener_arrendamientos())
     return JSONResponse(content=rents)

@rentRouter.get("/{id}", response_model=Rent)
async def rent(id: str):
    rent = dbConnection.obtener_arrendamiento_por_id(int(id))
    rent_dict = rent_schema(rent)
    return JSONResponse(content=rent_dict)

@rentRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Rent)
async def rent(rent: rent):
    rent_dict = dict(rent)
    del rent_dict["idArrendamiento"]
    dbConnection.agregar_arrendatario(**rent_dict)
    rent_dict = rent_schema(dbConnection.obtener_arrendatario_por_correo(rent.correo))
    return JSONResponse(content=rent_dict)

@rentRouter.delete("/{id}", status_code=status.HTTP_200_OK, response_model=Rent)
async def rent(id: str):
    rent_tuple = dbConnection.obtener_arrendamiento_por_id(int(id))
    rent_dict = rent_schema(rent_tuple)
    dbConnection.eliminar_arrendamiento(rent_dict["idArrendamiento"])
    return JSONResponse(content=rent_dict)

