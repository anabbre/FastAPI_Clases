import requests

# Dirección de la API local
url_base = "http://127.0.0.1:8000/teachers/"

#Añadir un nuevo profesor (POST)
new_teacher = {
    "id": 1,
    "name": "Ana Belén",
    "speciality": "Matemáticas"
}

response = requests.post(url_base, json=new_teacher) 
print(f"[POST] Código de respuesta: {response.status_code}")
print("Respuesta:", response.json())

#Obtener todos los profesores (GET)
response = requests.get(url_base)
print(f"\n[GET all] Código de respuesta: {response.status_code}")
print("Profesores:", response.json())

#Buscar profesor por ID (GET)
teacher_id = 1
response = requests.get(url_base + str(teacher_id))
print(f"\n[GET by ID] Código de respuesta: {response.status_code}")
print("Profesor:", response.json())

#Eliminar profesor por ID (DELETE)
response = requests.delete(url_base + str(teacher_id))
print(f"\n[DELETE] Código de respuesta: {response.status_code}")
print("Mensaje:", response.json())