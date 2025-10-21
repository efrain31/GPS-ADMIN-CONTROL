from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from models.fallas import Falla
from schemas.falla import FallaCreate, FallaRead
from utils.notificaciones import crear_notificacion
from utils.deps import get_current_user

router = APIRouter(prefix="/fallas", tags=["Fallas"])

# -------------------- Mapper de relaciones --------------------
def map_falla_relations(falla: Falla) -> FallaRead:
    return FallaRead(
        id=falla.id,
        descripcion=falla.descripcion,
        servicios=[s.id for s in getattr(falla, "servicios", [])]  
    )

# -------------------- Endpoints --------------------

# Select fallas (id + descripcion)
@router.get("/selectfalla", response_model=List[dict])
def select_fallas(db: Session = Depends(get_db)):
    fallas = db.query(Falla.id, Falla.descripcion).all()
    return [{"id": f.id, "descripcion": f.descripcion} for f in fallas]

# Listar todas las fallas con relaciones
@router.get("/all", response_model=List[FallaRead])
def get_fallas(db: Session = Depends(get_db)):
    fallas = db.query(Falla).options(joinedload(Falla.servicios)).all()
    return [map_falla_relations(f) for f in fallas]

# Obtener falla por ID
@router.get("/{falla_id}", response_model=FallaRead)
def get_falla_by_id(falla_id: int, db: Session = Depends(get_db)):
    falla = db.query(Falla).filter(Falla.id == falla_id).first()
    if not falla:
        raise HTTPException(status_code=404, detail="Falla no encontrada")
    return map_falla_relations(falla)

# Crear falla
@router.post("/crear", response_model=FallaRead)
def create_falla(falla: FallaCreate, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    nueva = Falla(**falla.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    crear_notificacion(
        db, 
        usuario_id=usuario.id, 
        mensaje=f"Falla creada: {nueva.descripcion}", 
        tipo="falla", 
        referencia_id=nueva.id
    )
    return map_falla_relations(nueva)

# Actualizar falla
@router.put("/actualizar{falla_id}", response_model=FallaRead)
def update_falla(falla_id: int, falla_update: FallaCreate, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    falla = db.get(Falla, falla_id)
    if not falla:
        raise HTTPException(status_code=404, detail="Falla no encontrada")
    for key, value in falla_update.dict().items():
        setattr(falla, key, value)
    db.commit()
    db.refresh(falla)
    crear_notificacion(
        db, 
        usuario_id=usuario.id, 
        mensaje=f"Falla actualizada: {falla.descripcion}", 
        tipo="falla", 
        referencia_id=falla.id
    )
    return map_falla_relations(falla)

# Borrar falla
@router.delete("/borrar{falla_id}")
def delete_falla(falla_id: int, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    falla = db.get(Falla, falla_id)
    if not falla:
        raise HTTPException(status_code=404, detail="Falla no encontrada")
    crear_notificacion(
        db, 
        usuario_id=usuario.id, 
        mensaje=f"Falla eliminada: {falla.descripcion}", 
        tipo="falla", 
        referencia_id=falla.id
    )
    db.delete(falla)
    db.commit()
    return {"message": "Falla eliminada correctamente"}
