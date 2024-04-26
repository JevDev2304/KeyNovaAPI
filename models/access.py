from pydantic import BaseModel


class Access(BaseModel):
    idAccess: int | None
    Propiedad_idPropiedad: int
    Agente_idAgente: int
