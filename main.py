from fastapi import FastAPI,File, UploadFile
from routers.owner import ownerRouter
from routers.agent import agentRouter

from routers.furniture import furnitureRouter

from routers.room import roomRouter
from routers.property import propertyRouter
from routers.access import accessRouter

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow connections from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ownerRouter)
app.include_router(agentRouter)
app.include_router(furnitureRouter)

app.include_router(propertyRouter)
app.include_router(accessRouter)
app.include_router(roomRouter)

app.mount("/static", StaticFiles(directory="static"), name = "static")

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API Keynova para la gestión de muebles de arrendamientos!"}




