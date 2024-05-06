from fastapi import FastAPI,File, UploadFile
from routers.owner import ownerRouter
from routers.agent import agentRouter
from routers.tenant import tenantRouter
from routers.furniture import furnitureRouter
from routers.rent import rentRouter
from routers.room import roomRouter
from routers.property import propertyRouter
from routers.access import accessRouter

from routers.uploadFiles import filesRouter
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.include_router(ownerRouter)
app.include_router(agentRouter)
app.include_router(tenantRouter)
app.include_router(furnitureRouter)
app.include_router(filesRouter)
app.include_router(rentRouter)
app.include_router(propertyRouter)
app.include_router(accessRouter)
app.include_router(roomRouter)

app.mount("/static", StaticFiles(directory="static"), name = "static")

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API Keynova para la gestión de muebles de arrendamientos!"}




