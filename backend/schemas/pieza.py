from pydantic import BaseModel
from typing import List, Optional, Literal
from models.piezas import TipoPiezaEnum

# ---------- Base ----------
class PiezaBase(BaseModel):
    tipo: TipoPiezaEnum  
    id_opcion: int  # obligatorio
    nombre: str     # obligatorio
    descripcion: Optional[str] = None
    stock: Optional[int] = 0

# ---------- Crear ----------
class PiezaCreate(PiezaBase):
    pass

# ---------- Actualizar ----------
class PiezaUpdate(BaseModel):
    tipo: Optional[Literal['CAMARA', 'LECTORA', 'DISCO_DURO', 'CABLE', 'GPS']] = None
    id_opcion: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    stock: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

# ---------- Leer ----------
class PiezaRead(PiezaBase):
    id: int

    model_config = {
        "from_attributes": True
    }

# ---------- Select ----------
class PiezaSelect(BaseModel):
    id: int
    nombre: str

    model_config = {
        "from_attributes": True
    }

# ---------- Relaciones ----------
class PiezaReadWithRelations(PiezaRead):
    inventario_interno: Optional[List[int]] = [] 
    servicio_piezas: Optional[List[int]] = []

