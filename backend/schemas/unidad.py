from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from .empresa import EmpresaRead
from .inventario_interno import InventarioInternoRead
from .log_falla import LogFallaRead
from .servicio import ServicioRead

# Solo para tipado y evitar import circular
if TYPE_CHECKING:
    from .planta import PlantaRead

class UnidadBase(BaseModel):
    tipo: str
    caracteristicas: Optional[str] = None
    ignicion_movimiento: Optional[str] = None
    empresa_id: Optional[int] = None
    planta_id: Optional[int] = None  # FK

class UnidadCreate(UnidadBase):
    pass

class UnidadRead(UnidadBase):
    id: int

    model_config = {"from_attributes": True}

class UnidadReadWithRelations(UnidadRead):
    empresa: Optional[EmpresaRead] = None
    planta: Optional["PlantaRead"] = None  # Forward reference como string

    inventario: Optional[List[InventarioInternoRead]] = None
    logs_fallas: Optional[List[LogFallaRead]] = None
    servicios: Optional[List[ServicioRead]] = None

# --- Resolver forward references al final ---
if TYPE_CHECKING is False:
    from .planta import PlantaRead
    UnidadReadWithRelations.model_rebuild()
