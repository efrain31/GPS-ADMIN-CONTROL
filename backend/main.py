from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import get_routers
import models  

from routes.auth import router as auth_router
from routes.usuarios import router as usuarios_router

app = FastAPI(title="Proyecto API")

Base.metadata.create_all(bind=engine)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      
    allow_credentials=True,
    allow_methods=["*"],       
    allow_headers=["*"],        
)
for router in get_routers():
    app.include_router(router)

app.include_router(auth_router)
app.include_router(usuarios_router)


@app.get("/")
def root():
    return {"msg": "API funcionando"}
