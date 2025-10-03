from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.servicios import Servicio
from schemas.servicio import ServicioCreate, ServicioRead, ServicioReadWithRelations
from utils.notificaciones import crear_notificacion
router = APIRouter(prefix="/servicios", tags=["Servicios"])

def map_servicio_relations(servicio: Servicio) -> ServicioReadWithRelations:
    return ServicioReadWithRelations(
        **servicio.__dict__,
        unidad=servicio.unidad.id if servicio.unidad else None,
        usuario_levanta=servicio.usuario_levanta.id if servicio.usuario_levanta else None,
        usuario_aprueba=servicio.usuario_aprueba.id if servicio.usuario_aprueba else None,
        pendientes=[p.id for p in servicio.pendientes],     
        fallas=[f.falla_id for f in servicio.fallas],      
        piezas=[p.pieza_id for p in servicio.piezas],       
        historial=[h.id for h in servicio.historial],       
        evidencias=[e.evidencia_id for e in servicio.evidencias], 
        tiempos=[t.id for t in servicio.tiempos],          
        extensiones=[ex.id for ex in servicio.extensiones]   
    )

@router.get("/", response_model=List[ServicioReadWithRelations])
def get_servicios(db: Session = Depends(get_db)):
    servicios = db.query(Servicio).all()
    return [map_servicio_relations(s) for s in servicios]


@router.get("/{servicio_id}", response_model=ServicioReadWithRelations)
def get_servicio(servicio_id: int, db: Session = Depends(get_db)):
    servicio = db.query(Servicio).filter(Servicio.id == servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return map_servicio_relations(servicio)


@router.post("/", response_model=ServicioReadWithRelations)
def create_servicio(servicio: ServicioCreate, db: Session = Depends(get_db)):
    nuevo_servicio = Servicio(**servicio.dict())
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)

    crear_notificacion(
        db,
        usuario_id=1,  # ajusta según usuario
        mensaje=f"Nuevo servicio {nuevo_servicio.id} creado",
        tipo="servicio",
        referencia_id=nuevo_servicio.id
    )

    return map_servicio_relations(nuevo_servicio)


@router.put("/{servicio_id}", response_model=ServicioReadWithRelations)
def update_servicio(servicio_id: int, servicio_update: ServicioCreate, db: Session = Depends(get_db)):
    servicio = db.query(Servicio).filter(Servicio.id == servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    for key, value in servicio_update.dict().items():
        setattr(servicio, key, value)

    db.commit()
    db.refresh(servicio)

    crear_notificacion(
        db,
        usuario_id=1,
        mensaje=f"Servicio {servicio.id} actualizado",
        tipo="servicio",
        referencia_id=servicio.id
    )

    return map_servicio_relations(servicio)


@router.delete("/{servicio_id}")
def delete_servicio(servicio_id: int, db: Session = Depends(get_db)):
    servicio = db.query(Servicio).filter(Servicio.id == servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    crear_notificacion(
        db,
        usuario_id=1,
        mensaje=f"Servicio {servicio.id} eliminado",
        tipo="servicio",
        referencia_id=servicio.id
    )

    db.delete(servicio)
    db.commit()

    return {"message": "Servicio eliminado correctamente"}

