from pydantic import BaseModel


class Owner (BaseModel):
    idPropietario: int | None
    nombre: str
    correo: str
    edad: int
    genero: str
    contrasennia: str
