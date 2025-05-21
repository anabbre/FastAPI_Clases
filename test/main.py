from database import Base, engine
from database import SessionLocal
from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel, Field, field_validator, model_validator
import logging
from typing import Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import Clases_db, Student               # importa tus modelos de tablas de database.py
import models



# Crear las tablas al iniciar
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)



# Validacion tabla "CLASES"
class Clases(BaseModel):
    name_clase: str = Field(..., description="Nombre de la Clase")
    año_clase: int = Field(None, ge=0, description="Año de curso de la Clase(Opcional)")

    @field_validator("name_clase")
    def clase_listada(cls, clase):
        lista_valida = ["mates", "literatura", "ingles", "musica", "plastica", "sociales", "economia", "historia", "filosofia"]
        if clase not in lista_valida:
            raise ValueError("Solo se pueden impartir estas clases: mates, literatura, ingles, musica, plastica, sociales, economia, historia, filosofia(en minusculas)")
        return clase

    @model_validator(mode="after")
    def año_caducado(cls, not_caducado):
        if not_caducado.año_clase <= 2024:
            raise ValueError("No se puede registrar un nuevo curso para que comiece antes de 2024")
        return not_caducado


# Validacion tabla "ESTUDIANTES"
class Student(BaseModel):
    nombre: str
    apellido: str
    edad: Optional[int] = None
    clase_id: Optional[int] = None


# Validacion tabla "PROFESORES"
class Teacher(BaseModel):
    id: int #identificador único de cada profesor 
    name: str = Field(..., min_length=3, description="Nombre del profesor") 
    speciality: str = Field(..., description="Especialidad del profesor") 




# Ejecutar app
app = FastAPI()

# Función para manejar los errores ValueError
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}  # Mostramos el mensaje de error
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response Status: {response.status_code}")
    return response











# APIs


#@#@#@#@#@#@#  CLASES   #@#@#@#@#@#@

@app.get("/")
def initial_greeting():
    logger.info(f"Recibido Peticion --CONEXION EXITOSA--")
    return {"message" : "Ha encontrado las clases!!"}


@app.get("/clases/{name}")
def mostrar_clases(name: str):
    logger.info(f"Ha encontrado la --CLASE DE {name.upper()}--")
    proceso_minus = "Clase de " + name
    return {"clase": f"Estas en la clase de {proceso_minus}"}


@app.post("/clases/")
def create_clase(name: Clases):
    logger.info(f"--La clase {name} se ha REGISTRADO CORRECTAMENTE--")
        ## Registrarlo de DDBB....

    db = SessionLocal()
    existe = db.query(Clases_db).filter(Clases_db.name_clase == name.name_clase).first()
    if existe:
        db.close()
        raise HTTPException(status_code=400, detail="La clase ya está registrada")
    
    clase_db = Clases_db(name_clase=name.name_clase, año_clase=name.año_clase)
    db.add(clase_db)
    db.commit()
    db.refresh(clase_db)
    db.close()
    
    
    
    return {   
        "msg": "Clase registrada correctamente",
        "Clase": name.name_clase
    }












#@#@#@#@#@#   ESTUDIANTES   #@#@#@#@#@#@

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

# POST
@app.post("/students")
def create_user(student: Student):
    student_id = max(students_sample.keys()) + 1
    clases = 1 if student.clase_id else 0
    logging.info(f"Nuevo usuario creado: {student.nombre} - {student.apellido} y se ha matriculado en {clases} clases")
    return {"msg": "Usuario creado correctamente", "con id": student_id}

@app.post("/students/search")
def search_student(student: Student, db: Session = Depends(get_db)):
#Buscar solo por nombre y apellido
    db_user = db.query(models.Student).filter(models.Student.surname == student.apellido).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Student already registered")

    # Crear instancia de User y guardar en base de datos
    # new_user = models.Student(**student.dict())
    new_user = models.Student(name=student.nombre, surname=student.apellido)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # refrescar para obtener el ID
    db.close()

    return new_user












#@#@#@#@#@#@#     PROFESORES    #@#@#@#@#@#@#@

from typing import List           # Eliminar cuando se crea Database en models
teachers_db: List[Teacher] = []   # ''


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