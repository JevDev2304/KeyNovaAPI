import uvicorn
from fastapi import FastAPI, Request, HTTPException
from routers.owner import ownerRouter
from routers.agent import agentRouter
from fastapi.responses import JSONResponse
from routers.furniture import furnitureRouter
from tools.jwt_auth_agent import verify_jwt_token
from routers.room import roomRouter
from routers.property import propertyRouter
from routers.access import accessRouter
from routers.maintenance import maintenancesRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000","http://127.0.0.1:5173","http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ownerRouter)
app.include_router(agentRouter)
app.include_router(furnitureRouter)
app.include_router(maintenancesRouter)
app.include_router(propertyRouter)
app.include_router(accessRouter)
app.include_router(roomRouter)

app.mount("/static", StaticFiles(directory="static"), name="static")





@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API Keynova para la gestión de muebles de arrendamientos!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info", use_colors=True)