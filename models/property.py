from pydantic import BaseModel

class Property(BaseModel):
    idPropiedad: int | None
    Propietario_cedula : int
    direccion: str
    tipo: str
