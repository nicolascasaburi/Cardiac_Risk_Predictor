import requests
import json
import time

# Cargar los primeros 10 datos del archivo JSON
with open("datos_generados.json", "r") as archivo:
    datos = json.load(archivo)[:10]

# URL del microservicio user_service
url_microservicio = "http://127.0.0.1:5000/user_service"

# Test con un usuario Freemium
headers = {
            'Authorization': '741f24cf76d772b15dcdd896d6044812',
            'Content-Type': 'application/json',
        }

# Enviar cada dato como una solicitud POST al microservicio
print("=" * 50)
print("Test de 10 llamados al microservicio user_service con un usuario Freemium")
for i, dato in enumerate(datos, start=1):
    respuesta = requests.post(url_microservicio, json=dato, headers=headers)

    # Imprimir la respuesta del microservicio
    print(f"Solicitud POST enviada para el dato: {dato}")
    print(f"Respuesta del microservicio: {respuesta.text}")
    print("=" * 50)
  # Agregar un retardo de 50 segundos después del llamado número 6
    if i == 6:
        print("Esperando 50 segundos...")
        time.sleep(50)

print("Todas las solicitudes POST han sido enviadas.")


# Cargar los primeros 60 datos del archivo JSON
with open("datos_generados.json", "r") as archivo:
    datos = json.load(archivo)[:60]

# URL del microservicio user_service
url_microservicio = "http://127.0.0.1:5000/user_service"

# Test con un usuario Premiun
headers = {
            'Authorization': '7803f9b4f94ab605f48087da2c2a1627',
            'Content-Type': 'application/json',
        }

# Enviar cada dato como una solicitud POST al microservicio
print("=" * 50)
print("Test de 60 llamados al microservicio user_service con un usuario Premium")
for i, dato in enumerate(datos, start=1):
    respuesta = requests.post(url_microservicio, json=dato, headers=headers)

    # Imprimir la respuesta del microservicio
    print(f"Solicitud POST enviada para el dato: {dato}")
    print(f"Respuesta del microservicio: {respuesta.text}")
    print("=" * 50)
  # Agregar un retardo de 50 segundos después del llamado númeroro 51
    if i == 51:
        print("Esperando 50 segundos...")
        time.sleep(50)

print("Todas las solicitudes POST han sido enviadas.")
