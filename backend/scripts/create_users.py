from utils.auth import hash_password
from database import SessionLocal
from models.usuarios import Usuario

db = SessionLocal()

email = "admin@prueba.com" #CAMBIA POR TUS DATOS

usuario_existente = db.query(Usuario).filter(Usuario.email == email).first()

if not usuario_existente:
    nuevo_usuario = Usuario(
        nombre="admin", #CAMBIA POR TUS DATOS
        email=email,
        password=hash_password("admin134679"), #CAMBIA POR TUS DATOS
        rol_id=2,  # asegúrate que ese rol exista en tu tabla roles O CREALO
        activo=True
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    print("Usuario creado:", nuevo_usuario.id)
else:
    print("El usuario ya existe:", usuario_existente.id)

db.close()


#COMANDO PARA EJECUTARLO EN LA TERMINAL 
#  python -m scripts.create_users