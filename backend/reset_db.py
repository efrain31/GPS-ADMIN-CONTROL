from database import Base, engine
import models  

print("Eliminando todas las tablas...")
Base.metadata.drop_all(bind=engine)  # elimina todas las tablas
print("Tablas eliminadas.")

print("Creando todas las tablas nuevamente...")
Base.metadata.create_all(bind=engine)  # crea todas las tablas DE NUEVO
print("Tablas creadas correctamente.")
