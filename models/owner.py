from pydantic import BaseModel


class Owner (BaseModel):
    idPropietario: int | None
    nombre: str
    correo: str
    genero: str
    contrasennia: str
    agente_idAgente: int
    cedula : str
    celular : str