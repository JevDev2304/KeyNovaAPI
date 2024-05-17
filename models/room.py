from pydantic import BaseModel

class Room(BaseModel):
    idHabitacion: int | None
    Propiedad_idPropiedad : int
    imagen: str
    nombre: str
    descripcion: str | None

