#API de cursos
#End points: listado de clases, profesores, estudiantes

from fastapi import FastAPI, Request, Depends, HTTPException
import logging
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

# Crear las tablas en la base de datos (solo una vez al inicio)
models.Base.metadata.create_all(bind=engine)

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Student(BaseModel):
    nombre: str
    apellido: str
    edad: Optional[int] = None
    clase_id: Optional[int] = None

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response Status: {response.status_code}")
    return response

students_sample = {
    1: {"nombre": "Ana", "apellido": "García", "edad": 20, "clase_id": 101},
    2: {"nombre": "Luis", "apellido": "Pérez", "edad": 22, "clase_id": 102},
    3: {"nombre": "María", "apellido": "López", "edad": 19, "clase_id": 101},
    4: {"nombre": "Carlos", "apellido": "Ramírez", "edad": 21, "clase_id": 103},
    5: {"nombre": "Sofía", "apellido": "Torres", "edad": 23, "clase_id": 102},
    6: {"nombre": "Javier", "apellido": "Díaz", "edad": 20, "clase_id": 103},
    7: {"nombre": "Lucía", "apellido": "Fernández", "edad": 18, "clase_id": 101},
    8: {"nombre": "Andrés", "apellido": "Morales", "edad": 22, "clase_id": 104},
    9: {"nombre": "Valentina", "apellido": "Ruiz", "edad": 21, "clase_id": 102},
    10: {"nombre": "Diego", "apellido": "Castro", "edad": 19, "clase_id": 104}
}

@app.get("/students/{id}")
def student_info(id:int):
    logger.info("Accessing student info")
    student = students_sample.get(id)
    if not student:
        return {"error": "Estudiante no encontrado"}
    return {
    "mensaje": f"Hola {student['nombre']} {student['apellido']}, usted está matriculado en la clase {student['clase_id']}"
}

@app.post("/students")
def create_user(student: Student):
    student_id = max(students_sample.keys()) + 1
    clases = 1 if student.clase_id else 0
    logging.info(f"Nuevo usuario creado: {student.nombre} - {student.apellido} y se ha matriculado en {clases} clases")
    return {"msg": "Usuario creado correctamente", "con id": student_id}

@app.post("/students/search")
def search_student(student: Student, db: Session = Depends(get_db)):
#Buscar solo por nombre y apellido
    db_user = db.query(models.Student).filter(models.Student.surname == student.surname).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Student already registered")

        # Crear instancia de User y guardar en base de datos
        new_user = models.Student(**student.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # refrescar para obtener el ID
        dc.close()
        return new_user



