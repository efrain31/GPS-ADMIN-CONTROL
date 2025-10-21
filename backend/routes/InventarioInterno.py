from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import Dict, List

from database import get_db
from models.inventario_interno import InventarioInterno
from models.unidades import Unidad
from models.piezas import Pieza
from models.usuarios import Usuario
from schemas.inventario_interno import (
    InventarioInternoCreate,
    InventarioInternoReadWithRelations,
    InventarioInternoUpdate,
)
from schemas.notificacione import NotificacionRead
from utils.notificaciones import crear_notificacion
from utils.deps import get_current_user

router = APIRouter(prefix="/inventario", tags=["InventarioInterno"])

# --- Mapear relaciones de inventario ---
def map_inventario_relations(inventario: InventarioInterno) -> InventarioInternoReadWithRelations:
    return InventarioInternoReadWithRelations(
        id=inventario.id,
        unidad_id=inventario.unidad_id,
        pieza_id=inventario.pieza_id,
        cantidad=inventario.cantidad,
        danado=inventario.danado,
        
        # Mostrar nombre/tipo junto con IDs
        unidad={"id": inventario.unidad.id, "nombre": inventario.unidad.tipo} if inventario.unidad else None,
        pieza={"id": inventario.pieza.id, "tipo": inventario.pieza.tipo} if inventario.pieza else None,

        registros=[r.id for r in getattr(inventario, "registros", [])],
        notificaciones=[NotificacionRead.from_orm(n) for n in getattr(inventario, "notificaciones", [])]
    )

# --- Obtener todos los inventarios ---
@router.get("/", response_model=List[InventarioInternoReadWithRelations])
def get_inventarios(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    inventarios = (
        db.query(InventarioInterno)
        .options(joinedload(InventarioInterno.unidad), joinedload(InventarioInterno.pieza))
        .all()
    )
    return [map_inventario_relations(i) for i in inventarios]


# --- Obtener inventario por ID ---
@router.get("/{inventario_id}", response_model=InventarioInternoReadWithRelations)
def get_inventario(inventario_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    inventario = (
        db.query(InventarioInterno)
        .options(joinedload(InventarioInterno.unidad), joinedload(InventarioInterno.pieza))
        .filter(InventarioInterno.id == inventario_id)
        .first()
    )
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return map_inventario_relations(inventario)


# --- Crear inventario ---
@router.post("/", response_model=InventarioInternoReadWithRelations)
def create_inventario(inventario: InventarioInternoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.rol_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear inventario")

    nuevo_inventario = InventarioInterno(
        unidad_id=inventario.unidad_id,
        pieza_id=inventario.pieza_id,
        cantidad=inventario.cantidad,
        danado=inventario.danado
    )

    db.add(nuevo_inventario)
    db.commit()
    db.refresh(nuevo_inventario)

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Inventario {nuevo_inventario.id} creado",
        tipo="inventario",
        referencia_id=nuevo_inventario.id
    )

    return map_inventario_relations(nuevo_inventario)


# --- Actualizar inventario ---
@router.put("/{inventario_id}", response_model=InventarioInternoReadWithRelations)
def update_inventario(inventario_id: int, inventario_update: InventarioInternoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    inventario = db.query(InventarioInterno).filter(InventarioInterno.id == inventario_id).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")

    if current_user.rol_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar inventario")

    update_data = inventario_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(inventario, key, value)

    db.commit()
    db.refresh(inventario)

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Inventario {inventario.id} actualizado",
        tipo="inventario",
        referencia_id=inventario.id
    )

    return map_inventario_relations(inventario)


# --- Eliminar inventario ---
@router.delete("/{inventario_id}")
def delete_inventario(inventario_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    inventario = db.query(InventarioInterno).filter(InventarioInterno.id == inventario_id).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")

    if current_user.rol_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar inventario")

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Inventario {inventario.id} eliminado",
        tipo="inventario",
        referencia_id=inventario.id
    )

    db.delete(inventario)
    db.commit()
    return {"message": "Inventario eliminado correctamente"}


@router.get("/select/unidades", response_model=List[Dict[str, str]])
def get_unidades_select(db: Session = Depends(get_db)):
    unidades = db.query(Unidad.id, Unidad.tipo).all()
    return [{"id": str(u.id), "nombre": u.tipo} for u in unidades]

@router.get("/select/piezas", response_model=List[Dict[str, str]])
def get_piezas_select(db: Session = Depends(get_db)):
    piezas = db.query(Pieza.id, Pieza.nombre).all()
    return [{"id": str(p.id), "nombre": p.nombre} for p in piezas]
