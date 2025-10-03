from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class InventarioInternoBase(BaseModel):
    unidad_id: int
    pieza_id: int
    cantidad: Optional[int] = 1
    danado: Optional[bool] = False
    fecha_actualizacion: Optional[datetime] = None

class InventarioInternoCreate(InventarioInternoBase):
    pass

class InventarioInternoRead(InventarioInternoBase):
    id: int

    model_config = {
    "from_attributes": True
}


# ----------  relaciones ----------
class InventarioInternoReadWithRelations(InventarioInternoRead):
    unidad: Optional[int] = None 
    pieza: Optional[int] = None  
    registros: Optional[List[int]] = [] 