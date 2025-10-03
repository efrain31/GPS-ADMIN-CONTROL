from pydantic import BaseModel
from typing import Optional

class ServicioPiezaBase(BaseModel):
    servicio_id: int
    pieza_id: int
    cantidad: Optional[int] = 1

class ServicioPiezaCreate(ServicioPiezaBase):
    pass

class ServicioPiezaRead(ServicioPiezaBase):
    
    
    
    
   model_config = {
    "from_attributes": True
}


# ----------  relaciones ----------
class ServicioPiezaReadWithRelations(ServicioPiezaRead):
    servicio: Optional[int] = None 
    pieza: Optional[int] = None    
