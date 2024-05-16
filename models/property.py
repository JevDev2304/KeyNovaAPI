from pydantic import BaseModel

class Property(BaseModel):
    idPropiedad: int | None
    Propietario_idPropietario : int
    direccion: str
    imagen: str | None
