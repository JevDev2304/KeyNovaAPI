from pydantic import BaseModel


class Furniture (BaseModel):
    idMueble: int | None
    Habitacion_idHabitacion: int
    estado: int
    imagen: str
    descripcion: str
    nombre : str
