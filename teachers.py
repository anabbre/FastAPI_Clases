from fastapi import FastAPI, APIRouter, Request, HTTPException, Depends #Importar FastAPI para crear la API y tipos necesarios para manejar peticiones y errores
from fastapi.responses import JSONResponse #Devuelve una respuesta personalizada JSON 
from pydantic import BaseModel, Field #BaseModel para crear el esquema de datos, Field para validar
from typing import List #para declarar listas de profesores
import logging #para mostrar mensajes por consola 

from sqlalchemy.orm import Session #Para interactuar con la base de datos 
from database import SessionLocal #importamos la sesión de la BD
from models import TeacherDB #y el modelo SQLAlchemy

# Configuración del logs
logging.basicConfig(
    level=logging.INFO, #mensajes de tipo INFO o superior
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s" #Formato de los mensajes
)
logger = logging.getLogger(__name__) #creamos el logger con el nombre del archivo 

#Modelo Pydantic para validar datos al enviar o recibir profesores
class Teacher(BaseModel):
    id: int #identificador único de cada profesor 
    name: str = Field(..., min_length=3, description="Nombre del profesor") 
    speciality: str = Field(..., description="Especialidad del profesor") 

    class Config:
        orm_mode = True #Convertir objetos de SQLAlchemy a JSON directamente

#Función para devolver una sesión de BD
def get_db():
    db = SessionLocal() #la crea
    try:
        yield db #se devuelve para usarla en las rutas
    finally:
        db.close() #cierra la sesión 

#Crear instancia del router para este módulo
router = APIRouter()  

#Raiz de la ruta de prueba para ver si la API funciona
@router.get("/")
async def root():
    logger.info("Root endpoint accessed") #Mostramos que alguien accedio 
    return {"message": "API de profesores funcionando correctamente!!"} 

#GET para listar todos los profesores
@router.get("teachers/", response_model=List[Teacher])
def list_teacher(db: Session = Depends(get_db)):
    logger.info("Se ha solicitado el listado de profesores")
    return db.query(TeacherDB).all() #Consultamos todos los registros 

#Añadir un nuevo profesor a la lista
@router.post("/teachers/", response_model=Teacher)
def create_teacher(teacher: Teacher, db: Session = Depends(get_db)):
    existing = db.query(TeacherDB).filter(TeacherDB.id == teacher.id).first()
    if existing:
        logger.warning(f"El profesor con ID {teacher.id} ya existe")
        raise HTTPException(status_code=400, detail="El ID ya está registrado")
    
    teacher_db = TeacherDB(**teacher.dict())
    db.add(teacher_db)
    db.commit()
    db.refresh(teacher_db)
    logger.info(f"Profesor creado: {teacher.name}")
    return teacher_db

#Buscar un profesor por ID
@router.get("/teachers/{teacher_id}", response_model=Teacher)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    logger.info(f"Buscando profesor con ID {teacher_id}")
    teacher = db.query(TeacherDB).filter(TeacherDB.id == teacher_id).first()
    if not teacher:
        logger.warning(f"Profesor con ID {teacher_id} no encontrado")
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    logger.info(f"Profesor encontrado: {teacher.name}")
    return teacher

#Eliminar un profesor por su ID
@router.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(TeacherDB).filter(TeacherDB.id == teacher_id).first()
    if not teacher:
        logger.warning(f"Intento de eliminar a un profesor inexistente con ID: {teacher_id}")
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    db.delete(teacher)  # Eliminamos el profesor
    db.commit()  # Confirmamos los cambios
    logger.info(f"Profesor eliminado: {teacher.name}")
    return {"message": "Profesor eliminado correctamente"}
