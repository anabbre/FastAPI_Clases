from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a SQLite (archivo local llamado test.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Crear el motor de la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear la sesión para hacer consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos ORM
Base = declarative_base()