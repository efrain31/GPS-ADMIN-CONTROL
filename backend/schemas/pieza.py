from pydantic import BaseModel
from typing import Optional, List, Literal

class PiezaBase(BaseModel):
    tipo: Literal['LECTORA', 'DISCO_DURO', 'CABLE', 'GPS']
    id_opcion: Optional[int] = None 
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    stock: Optional[int] = 0

class PiezaCreate(PiezaBase):
    pass

class PiezaRead(PiezaBase):
    id: int

    model_config = {
    "from_attributes": True
}


# ----------  relaciones ----------
class PiezaReadWithRelations(PiezaRead):
    inventario_interno: Optional[List[int]] = [] 
    servicio_piezas: Optional[List[int]] = []    
