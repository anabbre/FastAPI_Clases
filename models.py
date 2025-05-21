from sqlalchemy import Column, Integer, String
from database import Base

#Definir como se verá la tabla
class TeacherDB(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    speciality = Column(String, index=True)
