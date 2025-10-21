from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.piezas import Pieza, TipoPiezaEnum
from models.usuarios import Usuario
from schemas.pieza import PiezaCreate, PiezaReadWithRelations, PiezaUpdate
from schemas.notificacione import NotificacionRead
from utils.notificaciones import crear_notificacion
from utils.deps import get_current_user

router = APIRouter(prefix="/piezas", tags=["Piezas"])

# --- Mapear relaciones ---
def map_pieza_relations(pieza: Pieza) -> PiezaReadWithRelations:
    relacion = None
    if pieza.tipo == TipoPiezaEnum.CAMARA:
        relacion = pieza.camara
    elif pieza.tipo == TipoPiezaEnum.GPS:
        relacion = pieza.gps
    elif pieza.tipo == TipoPiezaEnum.LECTORA:
        relacion = pieza.lectora
    elif pieza.tipo == TipoPiezaEnum.DISCO_DURO:
        relacion = pieza.disco_duro
    elif pieza.tipo == TipoPiezaEnum.CABLE:
        relacion = pieza.cable

    return PiezaReadWithRelations(
        id=pieza.id,
        tipo=pieza.tipo.value,  # <-- aquí convertimos enum a string
        id_opcion=pieza.id_opcion,
        nombre=pieza.nombre,
        descripcion=pieza.descripcion,
        stock=pieza.stock,
        relacion=relacion,
        notificaciones=[NotificacionRead.from_orm(n) for n in getattr(pieza, "notificaciones", [])]
    )


# --- Obtener todas las piezas ---
@router.get("/", response_model=List[PiezaReadWithRelations])
def get_piezas(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    piezas = db.query(Pieza).all()
    return [map_pieza_relations(p) for p in piezas]

# --- Obtener pieza por ID ---
@router.get("/{pieza_id}", response_model=PiezaReadWithRelations)
def get_pieza(pieza_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    pieza = db.query(Pieza).filter(Pieza.id == pieza_id).first()
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    return map_pieza_relations(pieza)

# --- Crear pieza ---
@router.post("/", response_model=PiezaReadWithRelations)
def create_pieza(pieza: PiezaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.rol_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear piezas")

    nueva_pieza = Pieza(
        tipo=pieza.tipo,
        id_opcion=pieza.id_opcion,
        nombre=pieza.nombre,
        descripcion=pieza.descripcion,
        stock=pieza.stock
    )

    db.add(nueva_pieza)
    db.commit()
    db.refresh(nueva_pieza)

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Pieza {nueva_pieza.nombre} creada",
        tipo="pieza",
        referencia_id=nueva_pieza.id
    )

    return map_pieza_relations(nueva_pieza)

# --- Actualizar pieza ---
@router.put("/{pieza_id}", response_model=PiezaReadWithRelations)
def update_pieza(pieza_id: int, pieza_update: PiezaUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    pieza = db.query(Pieza).filter(Pieza.id == pieza_id).first()
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")

    if current_user.rol_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar piezas")

    update_data = pieza_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pieza, key, value)

    db.commit()
    db.refresh(pieza)

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Pieza {pieza.nombre} actualizada",
        tipo="pieza",
        referencia_id=pieza.id
    )

    return map_pieza_relations(pieza)

# --- Eliminar pieza ---
@router.delete("/{pieza_id}")
def delete_pieza(pieza_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    pieza = db.query(Pieza).filter(Pieza.id == pieza_id).first()
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")

    if current_user.rol_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar piezas")

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Pieza {pieza.nombre} eliminada",
        tipo="pieza",
        referencia_id=pieza.id
    )

    db.delete(pieza)
    db.commit()
    return {"message": "Pieza eliminada correctamente"}
