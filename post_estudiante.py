# import requests

# # URL base de tu app FastAPI (asegúrate de que esté corriendo)
# url = "http://127.0.0.1:8000/students"

# # Datos del usuario que vamos a enviar
# user_data = {
#     "nombre": "Paula",
#     "apellido": "Campreciós",
#     "edad": 30
# }

# # Hacer la petición POST
# response = requests.post(url, json=user_data)

# # Mostrar respuesta
# print("Status code:", response.status_code)
# print("Respuesta JSON:", response.json())

import requests

# URL base de tu app FastAPI (asegúrate de que esté corriendo)
url = "http://127.0.0.1:8000/students/search"

# Datos del usuario que vamos a enviar
user_data = {
    "nombre": "Paula",
    "apellido": "Campreciós",
    "edad": 30
}

# Hacer la petición POST
response = requests.post(url, json=user_data)

# Mostrar respuesta
print("Status code:", response.status_code)
print("Respuesta JSON:", response.json())