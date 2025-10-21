from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from database import get_db
from models.servicios import Servicio, EstadoServicioEnum, PrioridadEnum
from models.usuarios import Usuario
from schemas.servicio import ServicioCreate, ServicioReadWithRelations, ServicioUpdate
from schemas.servicio_pendiente import ServicioPendienteRead
from schemas.notificacione import NotificacionRead
from utils.notificaciones import crear_notificacion
from utils.deps import get_current_user

router = APIRouter(prefix="/servicios", tags=["Servicios"])

# --- Mapear relaciones ---
def map_servicio_relations(servicio: Servicio) -> ServicioReadWithRelations:
    return ServicioReadWithRelations(
        id=servicio.id,
        usuario_id_levanta=servicio.usuario_id_levanta,
        usuario_id_aprueba=servicio.usuario_id_aprueba,
        unidad_id=servicio.unidad_id,
        unidad_nombre=servicio.unidad.tipo if servicio.unidad else None,
        usuario_levanta_id=servicio.usuario_id_levanta,
        usuario_levanta_nombre=servicio.usuario_levanta.nombre if servicio.usuario_levanta else None,
        usuario_aprueba_id=servicio.usuario_id_aprueba,
        usuario_aprueba_nombre=servicio.usuario_aprueba.nombre if servicio.usuario_aprueba else None,
        planta=servicio.planta.nombre if servicio.planta else None,
        cambios=servicio.cambios,
        items=servicio.items,
        comentarios=servicio.comentarios,
        fecha_alta=servicio.fecha_alta,
        estado=servicio.estado.value if servicio.estado else None,
        prioridad=servicio.prioridad.value if servicio.prioridad else None,
        domiciliado=servicio.domiciliado,
        latitud=servicio.latitud,
        longitud=servicio.longitud,
        pendiente=servicio.pendiente,
        pendientes=[p.id for p in servicio.pendientes],
        notificaciones=[n.id for n in getattr(servicio, "notificaciones", [])]
    )


# --- Obtener todos los servicios ---
@router.get("/", response_model=List[ServicioReadWithRelations])
def get_servicios(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.rol_id == 3:  # Técnico
        servicios = db.query(Servicio).filter(
            (Servicio.usuario_id_levanta == current_user.id) |
            (Servicio.usuario_id_aprueba == current_user.id)
        ).all()
        return [map_servicio_relations(s) for s in servicios]

    servicios = db.query(Servicio).all()
    return [map_servicio_relations(s) for s in servicios]

# --- Obtener servicio por ID ---
@router.get("/{servicio_id}", response_model=ServicioReadWithRelations)
def get_servicio(servicio_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    servicio = db.query(Servicio).filter(Servicio.id == servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    if current_user.rol_id == 3 and servicio.usuario_id_aprueba != current_user.id and servicio.usuario_id_levanta != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este servicio")
    return map_servicio_relations(servicio)

# --- Crear servicio ---
@router.post("/", response_model=ServicioReadWithRelations)
def create_servicio(servicio: ServicioCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    nuevo_servicio = Servicio(
        usuario_id_levanta=current_user.id,
        usuario_id_aprueba=servicio.usuario_id_aprueba,
        unidad_id=servicio.unidad_id,
        planta_id=servicio.planta_id,
        cambios=servicio.cambios,
        items=servicio.items,
        comentarios=servicio.comentarios,
        fecha_alta=date.today(),
        estado=EstadoServicioEnum(servicio.estado) if servicio.estado else EstadoServicioEnum.PENDIENTE,
        prioridad=PrioridadEnum(servicio.prioridad) if servicio.prioridad else PrioridadEnum.MEDIA,
        domiciliado=servicio.domiciliado,
        latitud=servicio.latitud,
        longitud=servicio.longitud,
        pendiente=servicio.pendiente or False
    )

    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Nuevo servicio {nuevo_servicio.id} creado",
        tipo="servicio",
        referencia_id=nuevo_servicio.id
    )

    return map_servicio_relations(nuevo_servicio)

# --- Actualizar servicio ---
@router.put("/{servicio_id}", response_model=ServicioReadWithRelations)
def update_servicio(servicio_id: int, servicio_update: ServicioUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    servicio = db.query(Servicio).filter(Servicio.id == servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    update_data = servicio_update.dict(exclude_unset=True)

    # --- Convertir strings a Enum si vienen ---
    if "estado" in update_data and update_data["estado"] is not None:
        update_data["estado"] = EstadoServicioEnum(update_data["estado"])
    if "prioridad" in update_data and update_data["prioridad"] is not None:
        update_data["prioridad"] = PrioridadEnum(update_data["prioridad"])

    for key, value in update_data.items():
        setattr(servicio, key, value)

    db.commit()
    db.refresh(servicio)

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Servicio {servicio.id} actualizado",
        tipo="servicio",
        referencia_id=servicio.id
    )

    return map_servicio_relations(servicio)

# --- Eliminar servicio ---
@router.delete("/{servicio_id}")
def delete_servicio(servicio_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    servicio = db.query(Servicio).filter(Servicio.id == servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    if current_user.rol_id not in [1, 2]:  # Admin/SuperAdmin
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar servicios")

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Servicio {servicio.id} eliminado",
        tipo="servicio",
        referencia_id=servicio.id
    )

    db.delete(servicio)
    db.commit()
    return {"message": "Servicio eliminado correctamente"}
