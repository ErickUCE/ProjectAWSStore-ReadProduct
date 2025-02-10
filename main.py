from fastapi import FastAPI
from app.routes import router
from app.database import engine, Base

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI()

# Incluir las rutas
app.include_router(router)

@app.get("/")
def root():
    return {"message": "ReadProduct API is running!"}
