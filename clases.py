#################################################################
from fastapi import FastAPI, HTTPException
import logging
from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#################################################################

# Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)



# Base de datos sqlite
DATABASE_URL = "sqlite:///./clases.db" ###### Cambiarlo cuando juntemos las apis a una misma database pero difrentes tablas#########

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base  = declarative_base()

class Clases_db(Base):
    __tablename__ = "clases"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Autoincrementar
    name_clase = Column(String, unique=True, index=True)                    # Unica
    año_clase = Column(Integer, nullable=True)                              # Opcionals

Base.metadata.create_all(bind=engine)




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


#http://127.0.0.1:8000/docs http://127.0.0.1:8000/redoc
app = FastAPI(                       
    title = "API Clases",       
    version = "1.0"
)

# Mensaje de conectado correctamente
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