from pydantic import BaseModel


class Agent (BaseModel):
    idAgente: int | None
    nombre: str
    correo: str
    contrasennia: int
    tipo: str
