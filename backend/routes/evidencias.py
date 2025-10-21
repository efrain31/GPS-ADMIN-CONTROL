from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from models.evidencias import Evidencia
from schemas.evidencia import EvidenciaCreate, EvidenciaRead,EvidenciaReadWithRelations,ServicioEvidenciaReadWithRelations
from utils.notificaciones import crear_notificacion
from utils.deps import get_current_user

router = APIRouter(prefix="/evidencias", tags=["Evidencias"])

# -------------------- Mapper de relaciones --------------------
def map_evidencia_relations(e: Evidencia) -> EvidenciaReadWithRelations:
    return EvidenciaReadWithRelations(
        id=e.id,
        url_imagen=e.url_imagen,
        descripcion=e.descripcion,
        fecha=e.fecha,
        servicios=[ServicioEvidenciaReadWithRelations.from_orm(s) for s in e.servicios]  # mapea relaciones
    )


# -------------------- Endpoints --------------------

# Select evidencias (id + descripcion)
@router.get("/selectevidencia", response_model=List[dict])
def select_evidencias(db: Session = Depends(get_db)):
    evidencias = db.query(Evidencia.id, Evidencia.descripcion).all()
    return [{"id": e.id, "descripcion": e.descripcion} for e in evidencias]

# Listar todas las evidencias con relaciones
@router.get("/all", response_model=List[EvidenciaRead])
def get_evidencias(db: Session = Depends(get_db)):
    evidencias = db.query(Evidencia).options(joinedload(Evidencia.servicios)).all()
    return [map_evidencia_relations(e) for e in evidencias]

# Obtener evidencia por ID
@router.get("/{evidencia_id}", response_model=EvidenciaRead)
def get_evidencia_by_id(evidencia_id: int, db: Session = Depends(get_db)):
    e = db.query(Evidencia).filter(Evidencia.id == evidencia_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")
    return map_evidencia_relations(e)

# Crear evidencia
@router.post("/crear", response_model=EvidenciaRead)
def create_evidencia(evidencia: EvidenciaCreate, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    nueva = Evidencia(**evidencia.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    crear_notificacion(db, usuario_id=usuario.id, mensaje=f"Evidencia creada", tipo="evidencia", referencia_id=nueva.id)
    return map_evidencia_relations(nueva)

# Actualizar evidencia
@router.put("/actualizar{evidencia_id}", response_model=EvidenciaRead)
def update_evidencia(evidencia_id: int, evidencia_update: EvidenciaCreate, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    evidencia = db.get(Evidencia, evidencia_id)
    if not evidencia:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")
    for key, value in evidencia_update.dict().items():
        setattr(evidencia, key, value)
    db.commit()
    db.refresh(evidencia)
    crear_notificacion(db, usuario_id=usuario.id, mensaje=f"Evidencia actualizada", tipo="evidencia", referencia_id=evidencia.id)
    return map_evidencia_relations(evidencia)

# Borrar evidencia
@router.delete("/borrar{evidencia_id}")
def delete_evidencia(evidencia_id: int, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    evidencia = db.get(Evidencia, evidencia_id)
    if not evidencia:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")
    crear_notificacion(db, usuario_id=usuario.id, mensaje=f"Evidencia eliminada", tipo="evidencia", referencia_id=evidencia.id)
    db.delete(evidencia)
    db.commit()
    return {"message": "Evidencia eliminada correctamente"}
