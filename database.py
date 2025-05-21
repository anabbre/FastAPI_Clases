from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#URL de conexión (base de datos local SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" 

#Motor de base de datos para conectar con el archivo test.db
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necesario solo para SQLite
)

#Crear la sesión para hacer consultas a la API
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base para los modelos para definir las tablas 
Base = declarative_base()