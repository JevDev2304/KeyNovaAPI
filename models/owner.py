from pydantic import BaseModel


class Owner (BaseModel):
    idPropietario: int | None
    nombre: str
    correo: str
    genero: str
    contrasennia: str
