from pydantic import BaseModel
from typing import Optional, Literal

class LectoraBase(BaseModel):
    tipo: Optional[Literal['CODIGO', 'BARRAS', 'RFID']] = None  # valida los valores permitidos

class LectoraCreate(LectoraBase):
    pass

class LectoraRead(LectoraBase):
    id: int

    model_config = {
    "from_attributes": True
}

