# utils/servicio_ops.py
from sqlalchemy.orm import Session
from datetime import datetime
from models.servicios import Servicio
from models.servicio_historial import ServicioHistorial
from models.piezas import Pieza
from models.inventario_interno import InventarioInterno
from models.unidad_pieza_registro import UnidadPiezaRegistro
from models.servicio_pieza import ServicioPieza
from utils.notificaciones import crear_notificacion

def registrar_evento_servicio(db: Session, servicio_id: int, usuario_id: int, accion: str):
    """Registra evento en ServicioHistorial y opcionalmente crea notificación."""
    evento = ServicioHistorial(
        servicio_id=servicio_id,
        usuario_id=usuario_id,
        accion=accion,
        fecha=datetime.now()
    )
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento

def gestionar_stock(db: Session, pieza_id: int, cantidad: int, origen_inventario_id: int | None = None, usuario_id: int | None = None):
    """
    Descarga stock de Pieza y/o InventarioInterno.
    - Si origen_inventario_id se pasa, decrementa esa fila de inventario_interno.
    - Siempre decrementa Pieza.stock.
    Lanza Exception si no hay stock suficiente.
    """
    pieza = db.get(Pieza, pieza_id)
    if not pieza:
        raise ValueError("Pieza no encontrada")

    # Primero, si se indicó inventario interno, descontar allí
    if origen_inventario_id:
        inv = db.get(InventarioInterno, origen_inventario_id)
        if not inv:
            raise ValueError("Inventario interno no encontrado")
        if inv.cantidad < cantidad:
            raise ValueError("No hay suficiente cantidad en inventario interno")
        inv.cantidad -= cantidad
        db.add(inv)

    # Descontar del stock global (piezas.stock)
    if pieza.stock < cantidad:
        raise ValueError("No hay stock global suficiente")
    pieza.stock -= cantidad
    db.add(pieza)
    db.commit()
    # opcional: registrar movimiento en UnidadPiezaRegistro si se consume desde una unidad -> lo maneja quien llama
    return True

def devolver_stock(db: Session, pieza_id: int, cantidad: int, inventario_interno_id: int | None = None):
    """Devuelve stock global y opcionalmente al inventario_interno."""
    pieza = db.get(Pieza, pieza_id)
    if not pieza:
        raise ValueError("Pieza no encontrada")
    pieza.stock += cantidad
    db.add(pieza)
    if inventario_interno_id:
        inv = db.get(InventarioInterno, inventario_interno_id)
        if not inv:
            raise ValueError("Inventario interno no encontrado")
        inv.cantidad += cantidad
        db.add(inv)
    db.commit()
    return True
