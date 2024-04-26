from pydantic import BaseModel

class Tenant(BaseModel):
    idArrendatario: int | None
    nombre: str
    correo: str
    edad: int
    genero : str
