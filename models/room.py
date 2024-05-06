from pydantic import BaseModel

class Room(BaseModel):
    idHabitacion: int | None
    Propiedad_idPropiedad : int
    estado: str
    video: str
    nombre: str

