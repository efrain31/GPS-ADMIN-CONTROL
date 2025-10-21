from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UnidadPiezaRegistroBase(BaseModel):
    unidad_id: int
    inventario_id: int
    cantbus: Optional[str] = None
    danado: Optional[bool] = False
    fecha_actualizacion: Optional[datetime] = None
    usuario_id: Optional[int] = None
    motivo_cambio: Optional[str] = None

class UnidadPiezaRegistroCreate(UnidadPiezaRegistroBase):
    pass

class UnidadPiezaRegistroRead(UnidadPiezaRegistroBase):
    id: int

    model_config = {
    "from_attributes": True
}
class UnidadPiezaRegistroUpdate(BaseModel):
    cantbus: Optional[str] = None
    danado: Optional[bool] = None
    motivo_cambio: Optional[str] = None


# ----------  relaciones ----------
class UnidadPiezaRegistroReadWithRelations(UnidadPiezaRegistroRead):
    unidad: Optional[int] = None      
    inventario: Optional[int] = None     
    usuario: Optional[int] = None       
