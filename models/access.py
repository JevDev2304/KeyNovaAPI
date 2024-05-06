from pydantic import BaseModel


class Access(BaseModel):
    Propiedad_idPropiedad: int
    Agente_idAgente: int
