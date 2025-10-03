from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.usuarios import Usuario
from models.roles import Rol
from schemas.usuario import UsuarioCreate, UsuarioReadWithRelations, UsuarioUpdate
from schemas.servicio_pendiente import ServicioPendienteRead
from schemas.notificacione import NotificacionRead
from utils.notificaciones import crear_notificacion
from utils.auth import hash_password
from utils.deps import get_current_user 
from fastapi import status
from utils.auth import verify_password, create_access_token



router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# --- Mapear relaciones ---
def map_usuario_relations(usuario: Usuario) -> UsuarioReadWithRelations:
    empresa_id = usuario.unidad.empresa_id if usuario.unidad else None

    return UsuarioReadWithRelations(
        **usuario.__dict__,
        servicios_levantados=[s.id for s in usuario.servicios_levantados],
        servicios_aprobados=[s.id for s in usuario.servicios_aprobados],
        servicio_historial=[s.id for s in usuario.servicio_historial],
        tiempos_servicios=[t.id for t in usuario.tiempos_servicios],
        extensiones_servicios=[e.id for e in usuario.extensiones_servicios],
        piezas_registro=[p.id for p in usuario.piezas_registro],

        notificaciones=[
            NotificacionRead.from_orm(n)
            for n in usuario.notificaciones
            if n.tipo != "empresa" or n.referencia_id == empresa_id
        ],
        pendientes_asignados=[ServicioPendienteRead.from_orm(p) for p in usuario.pendientes_asignados],
        pendientes_tecnico=[ServicioPendienteRead.from_orm(p) for p in usuario.pendientes_tecnico]
    )

@router.get("/me", response_model=UsuarioReadWithRelations)
def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    return map_usuario_relations(current_user)


@router.get("/", response_model=List[UsuarioReadWithRelations])
def get_usuarios(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.rol_id == 3:  # Técnico solo ve su info TECNICO NIVEL (3)
        return [map_usuario_relations(current_user)]
    usuarios = db.query(Usuario).all()
    return [map_usuario_relations(u) for u in usuarios]

@router.get("/{usuario_id}", response_model=UsuarioReadWithRelations)
def get_usuario(usuario_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if current_user.rol_id == 3 and current_user.id != usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este usuario")
    return map_usuario_relations(usuario)


# --- Crear usuario público (Técnico por defecto) ---
@router.post("/", response_model=UsuarioReadWithRelations)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existing_user:
        if not verify_password(usuario.password, existing_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya existe y la contraseña no coincide"
            )
        return map_usuario_relations(existing_user)

    hashed_pw = hash_password(usuario.password)
    usuario_data = usuario.dict(exclude={"password", "rol_id"})
    nuevo_usuario = Usuario(**usuario_data, password=hashed_pw, rol_id=3) 

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    crear_notificacion(
        db,
        usuario_id=nuevo_usuario.id,  
        mensaje=f"Nuevo usuario {nuevo_usuario.nombre} creado",
        tipo="usuario",
        referencia_id=nuevo_usuario.id
    )
    return map_usuario_relations(nuevo_usuario)


# --- Crear usuario con rol (solo Admin/SuperAdmin) ---
@router.post("/with-rol/", response_model=UsuarioReadWithRelations)
def create_usuario_con_rol(
    usuario: UsuarioCreate,
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.rol_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="No tienes permiso para asignar roles")
    if rol_id == 1 and current_user.rol_id != 1:
        raise HTTPException(status_code=403, detail="Solo SuperAdmin puede crear otro SuperAdmin")

    existing_user = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existing_user:
        if not verify_password(usuario.password, existing_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya existe y la contraseña no coincide"
            )
        return map_usuario_relations(existing_user)

    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=400, detail="El rol especificado no existe")

    hashed_pw = hash_password(usuario.password)
    usuario_data = usuario.dict(exclude={"password"})
    nuevo_usuario = Usuario(**usuario_data, password=hashed_pw, rol_id=rol_id)

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Nuevo usuario {nuevo_usuario.nombre} creado con rol {rol.nombre}",
        tipo="usuario",
        referencia_id=nuevo_usuario.id
    )
    return map_usuario_relations(nuevo_usuario)

@router.put("/{usuario_id}/rol", response_model=UsuarioReadWithRelations)
def actualizar_rol(
    usuario_id: int,
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if current_user.rol_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="No tienes permiso para cambiar roles")
    if rol_id == 1 and current_user.rol_id != 1:
        raise HTTPException(status_code=403, detail="Solo SuperAdmin puede asignar rol SuperAdmin")

    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=400, detail="El rol especificado no existe")

    usuario.rol_id = rol_id
    db.commit()
    db.refresh(usuario)

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Rol de usuario {usuario.nombre} actualizado a {rol.nombre}",
        tipo="usuario",
        referencia_id=usuario.id
    )
    return map_usuario_relations(usuario)

@router.put("/{usuario_id}", response_model=UsuarioReadWithRelations)
def update_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = usuario_update.dict(exclude_unset=True, exclude={"rol_id", "password"})

    for key, value in update_data.items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Usuario {usuario.nombre} actualizado",
        tipo="usuario",
        referencia_id=usuario.id
    )

    return map_usuario_relations(usuario)

@router.delete("/{usuario_id}")
def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if current_user.rol_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar usuarios")

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Usuario {usuario.nombre} eliminado",
        tipo="usuario",
        referencia_id=usuario.id
    )

    db.delete(usuario)
    db.commit()

    return {"message": "Usuario eliminado correctamente"}
