from pydantic import BaseModel
from typing import Optional

class ServicioFallaBase(BaseModel):
    servicio_id: int
    falla_id: int

class ServicioFallaCreate(ServicioFallaBase):
    pass

class ServicioFallaRead(ServicioFallaBase):
    
    
    
    
    model_config = {
    "from_attributes": True
}


# ---------- relaciones ----------
class ServicioFallaReadWithRelations(ServicioFallaRead):
    servicio: Optional[int] = None  
    falla: Optional[int] = None     
