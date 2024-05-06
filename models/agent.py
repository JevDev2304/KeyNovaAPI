from pydantic import BaseModel


class Agent (BaseModel):
    idAgente: int | None
    tipo: str
    nombre: str
    correo: str
    contrasennia: int
    imagen : str

