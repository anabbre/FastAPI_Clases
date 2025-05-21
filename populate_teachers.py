from database import SessionLocal
from models import TeacherDB

# Crear sesión
db = SessionLocal()

# Lista de profesores de ejemplo
profesores = [
    TeacherDB(id=1, name="Ana Belén", speciality="Matemáticas"),
    TeacherDB(id=2, name="Luis Pérez", speciality="Física"),
    TeacherDB(id=3, name="Laura Gómez", speciality="Lengua"),
]

# Insertar si no existen
for profe in profesores:
    existe = db.query(TeacherDB).filter(TeacherDB.id == profe.id).first()
    if not existe:
        db.add(profe)

db.commit()
db.close()

print("Profesores insertados correctamente.")
