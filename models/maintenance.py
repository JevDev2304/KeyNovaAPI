from pydantic import BaseModel


class Maintenance (BaseModel):
    idMantenimiento: int | None
    Propiedad_idPropiedad: int
    descripcion: str
    fecha: str
    descripcion: str
