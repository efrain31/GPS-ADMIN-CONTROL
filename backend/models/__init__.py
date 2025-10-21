from database import Base

from .usuarios import Usuario
from .roles import Rol
from .empresas import Empresa
from .unidades import Unidad
from .planta import Planta

from .gps_modelos import GpsModelo
from .cables import Cable
from .discos_duros import DiscoDuro
from .lectoras import Lectora
from .piezas import Pieza 
from .camaras import Camara
from .inventario_interno import InventarioInterno
from .unidad_pieza_registro import UnidadPiezaRegistro

from .fallas import Falla
from .log_fallas import LogFalla

from .servicios import Servicio
from .servicio_evidencia import ServicioEvidencia
from .servicio_historial import ServicioHistorial
from .servicio_pieza import ServicioPieza
from .servicio_falla import ServicioFalla
from .servicio_pendiente import ServicioPendiente

from .evidencias import Evidencia
from .servicio_tiempo import ServicioTiempo
from .servicio_extension import ServicioExtension
from .notificaciones import Notificacion 

# Base.metadata.create_all(engine) podrá registrar todas las tablas
__all__ = [
    "Usuario", "Rol",
    "Empresa", "Unidad","PLanta",
    "Lectora", "DiscoDuro", "Cable", "GpsModelo", "Camara",
    "Pieza", "InventarioInterno", "UnidadPiezaRegistro",
    "Falla", "LogFalla",
    "Servicio", "ServicioPendiente", "ServicioFalla", "ServicioPieza", "ServicioHistorial", "ServicioEvidencia",
    "Evidencia",
    "ServicioTiempo", "ServicioExtension",'Notificacion'
]
