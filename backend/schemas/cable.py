from pydantic import BaseModel
from typing import Optional

class CableBase(BaseModel):
    estado: Optional[str] = None  # 'NUEVO', 'USADO', 'DANADO'

class CableCreate(CableBase):
    pass

class CableRead(CableBase):
    id: int



    model_config = {
    "from_attributes": True
}


