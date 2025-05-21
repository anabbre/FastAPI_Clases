import requests

url = "http://127.0.0.1:8000/clases/"

class_data = {
    "name_clase": "filosofia",
    "año_clase": 2026
}

response = requests.post(url, json=class_data)
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {response.json()}")