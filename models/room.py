from pydantic import BaseModel

class Room(BaseModel):
    idHabitacion: int | None
    Propietario_cedula : int
    direccion: str
    tipo: str
