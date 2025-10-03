from pydantic import BaseModel
from typing import Optional, Literal

class DiscoDuroBase(BaseModel):
    tipo: Optional[Literal['SSD', 'HDD', 'OTRO']] = None  # valida los valores permitidos

class DiscoDuroCreate(DiscoDuroBase):
    pass

class DiscoDuroRead(DiscoDuroBase):
    id: int

    model_config = {
    "from_attributes": True
}

