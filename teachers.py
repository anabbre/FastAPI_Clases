from fastapi import FastAPI, Request
from pydantic import BaseModel, Field #BaseModel para crear el esquema de datos, Field para validar
from typing import List #para declarar listas de profesores
import logging #para mostrar mensajes por consola 

# Configuración del logger
logging.basicConfig(
    level=logging.INFO, #mensajes de tipo INFO o superior
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s" #Formato de los mensajes
)
logger = logging.getLogger(__name__) #creamos el logger con el nombre del archivo 

app = FastAPI()

#Mostrar la información cada vez que llega una petición
@app.middleware("http")
async def log_requests(request: Request, call_next): 
    logger.info(f"Request: {request.method} {request.url}") #Log del tipo petición (GET, POST,...)
    response = await call_next(request) #Procesamos la respuesta
    logger.info(f"Response Status: {response.status_code}") #Log del código de respuesta
    return response

#Creamos el modelo Profesor
class Teacher(BaseModel):
    id: int #identificador único de cada profesor 
    name: str = Field(..., min_length=3, description="Nombre del profesor") 
    speciality: str = Field(..., description="Especialidad del profesor") 

#Simulación de la base de datos con la lista vacía
teachers_db: List[Teacher] = []

#Raiz de la ruta de prueba para ver si la API funciona
@app.get("/")
async def root():
    logger.info("Root endpoint accessed") #Mostramos que alguien accedio 
    return {"message": "API de profesores funcionando correctamente!!"} 

#GET para listar todos los profesores
@app.get("teachers/", response_model=List[Teacher])
async def list_teacher():
    logger.info("Se ha solicitado el listado de profesores")
    return teachers_db 

#Añadir un nuevo profesor a la lista
@app.post("/teachers/", response_model=Teacher)
async def create_teacher(teacher: Teacher):
    if any(t.id == teacher.id for t in teachers_db): #comprobación
        logger.warning(f"El profesor con ID {teacher.id} ya existe")
        raise ValueError("El ID del profesor ya está registrado")
    
    teachers_db.append(teacher)
    logger.info(f"Profesor añadido: {teacher.name} ({teacher.speciality})") 
    return teacher 

#Buscar un profesor por ID
@app.get("/teachers/{teacher_id}", response_model=Teacher)
async def get_teacher(teacher_id: int):
    for teacher in teachers_db: #recorrer la lista
        if teacher.id == teacher_id:
            logger.info(f"Profesor encontrado: {teacher.name}") 
            return teacher
    logger.warning(f"Profesor con ID {teacher_id} no encontrado")
    raise ValueError("Profesor no encontrado") 

#Eliminar un profesor por su ID
@app.delete("/teachers/¨teacher_id")
async def delete_teacher(teacher_id: int):
    for teacher in teachers_db:
        if teacher.id == teacher_id:
            teachers_db.remove(teacher)
            logger.info(f"Profesor eliminado: {teacher.name}")
            return {"message": "Profesor eliminado correctamente"}
    logger.warning(f"Intento de eliminar a un profesor inexistente con ID: {teacher_id}")
    raise ValueError("Profesor no encontrado")
