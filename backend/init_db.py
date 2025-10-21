from database import engine, Base
import models  # Importa todos tus modelos

def reset_db():
    print("Eliminando todas las tablas de la base de datos...")
    Base.metadata.drop_all(bind=engine)  # Esto elimina todas las tablas respetando FK
    print("Todas las tablas eliminadas correctamente.")

    print("Creando todas las tablas nuevamente...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas correctamente.")

if __name__ == "__main__":
    reset_db()
