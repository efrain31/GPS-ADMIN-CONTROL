from pydantic import BaseModel
from typing import Optional, List
from .empresa import EmpresaRead  
from .inventario_interno import InventarioInternoRead
from .log_falla import LogFallaRead
from .servicio import ServicioRead


class UnidadBase(BaseModel):
    tipo: str
    caracteristicas: Optional[str] = None
    ignicion_movimiento: Optional[str] = None
    empresa_id: Optional[int] = None


class UnidadCreate(UnidadBase):
    pass


class UnidadRead(UnidadBase):
    id: int

    model_config = {
        "from_attributes": True
    }


# ----------  relaciones ----------
class UnidadReadWithRelations(UnidadRead):
    empresa: Optional[EmpresaRead] = None
    inventario: Optional[List[InventarioInternoRead]] = []  
    logs_fallas: Optional[List[LogFallaRead]] = []  
    servicios: Optional[List[ServicioRead]] = []  
