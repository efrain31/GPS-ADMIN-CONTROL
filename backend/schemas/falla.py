from pydantic import BaseModel
from typing import Optional, List

class FallaBase(BaseModel):
    descripcion: str

class FallaCreate(FallaBase):
    pass

class FallaRead(FallaBase):
    id: int

    model_config = {
    "from_attributes": True
}


# ----------  relaciones ----------
class FallaReadWithRelations(FallaRead):
    logs: Optional[List[int]] = []         
    servicios: Optional[List[int]] = []    