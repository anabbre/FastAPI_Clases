from sqlalchemy import Column, Integer, String
from database import Base

# Modelo que representa la tabla "users"
class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)  # id autoincremental
    name = Column(String, index=True)
    surname = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=True)
    class_id = Column(Integer, nullable=True)


class Clases_db(Base):
    __tablename__ = "clases"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Autoincrementar
    name_clase = Column(String, unique=True, index=True)                    # Unica
    año_clase = Column(Integer, nullable=True)                              # Opcionals


