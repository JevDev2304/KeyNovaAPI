from fastapi import FastAPI, Request, HTTPException
from routers.owner import ownerRouter
from routers.agent import agentRouter
from fastapi.responses import JSONResponse
from routers.furniture import furnitureRouter
from tools.jwt_auth_agent import verify_jwt_token
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


@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    exclude_paths = ["/agent/login", "/", "/docs", "/openapi.json", "/static/images/"] # Rutas que no requieren token
    if not any(request.url.path.startswith(path) for path in exclude_paths):
        token = request.headers.get("Authorization")
        if token is None :
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})
        try:
            verify_jwt_token(token)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"message": e.detail})

    response = await call_next(request)
    return response

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API Keynova para la gestión de muebles de arrendamientos!"}




