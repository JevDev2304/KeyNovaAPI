from pydantic import BaseModel

class Rent(BaseModel):
    idArrendamiento: int | None
    Propiedad_idPropiedad: int
    Arrendatario_idArrendatario: int
    fecha_inicio: str
    fecha_final: str
