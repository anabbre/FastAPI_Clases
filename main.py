from fastapi import FastAPI, Request 
import logging

from models import Base
from database import engine
from teachers import router as teacher_router

# Crear las tablas en la base de datos (solo una vez al inicio)
Base.metadata.create_all(bind=engine)

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Crear instancia principal de FastAPI
app = FastAPI(
    title="API de Profesores",
    version="1.0"
)

#Middelware para registrar cada vez que llega una petición y su respuesta
@app.middleware("http")
async def log_requests(request: Request, call_next): 
    logger.info(f"Request: {request.method} {request.url}") #Log del tipo petición (GET, POST,...)
    response = await call_next(request) #Procesamos la respuesta
    logger.info(f"Response Status: {response.status_code}") #Log del código de respuesta
    return response

# Incluir el router de profesores
app.include_router(teacher_router)
