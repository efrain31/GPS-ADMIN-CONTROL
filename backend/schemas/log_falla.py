from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LogFallaBase(BaseModel):
    unidad_id: Optional[int] = None
    falla_id: Optional[int] = None
    descripcion: Optional[str] = None
    fecha_registro: Optional[datetime] = None
    activo: Optional[bool] = True

class LogFallaCreate(LogFallaBase):
    pass

class LogFallaRead(LogFallaBase):
    id: int

    model_config = {
    "from_attributes": True
}


# ----------  relaciones ----------
class LogFallaReadWithRelations(LogFallaRead):
    unidad: Optional[int] = None  
    falla: Optional[int] = None   
