from pydantic import BaseModel

class Property(BaseModel):
    idPropiedad: int | None
    Propietario_idPropietario : int
    direccion: str
    tipo: str
    imagen: str | None
