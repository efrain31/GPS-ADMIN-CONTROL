from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class InventarioInternoBase(BaseModel):
    unidad_id: int
    pieza_id: int
    cantidad: Optional[int] = 1
    danado: Optional[bool] = False
    fecha_actualizacion: Optional[datetime] = None

class InventarioInternoUpdate(BaseModel):
    unidad_id: Optional[int] = None
    pieza_id: Optional[int] = None
    cantidad: Optional[int] = None
    danado: Optional[bool] = None
    fecha_actualizacion: Optional[datetime] = None
    

    class Config:
        orm_mode = True

class InventarioInternoCreate(InventarioInternoBase):
    pass

class InventarioInternoRead(InventarioInternoBase):
    id: int

    model_config = {
    "from_attributes": True
}


# ----------  relaciones ----------
class InventarioInternoReadWithRelations(InventarioInternoRead):
    unidad: Optional[dict] = None  # antes era int
    pieza: Optional[dict] = None
    registros: Optional[List[int]] = []
