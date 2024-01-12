import requests
import json
import time


# TEST DEL microservicio authentication_service
# URL del microservicio user_service
url_microservicio = "http://127.0.0.1:5001/authentication_service"

# Test con un usuario Premium
headers = {
            'Authorization': '7803f9b4f94ab605f48087da2c2a1627',
            'Content-Type': 'application/json',
        }

respuesta = requests.post(url_microservicio, headers=headers)
print("=" * 50)
print("Test de llamados al microservicio authentication_service para un usuario Premium")
print(f"Respuesta del microservicio: {respuesta.text}")
print("=" * 50)

# Test con un usuario Freemium
headers = {
            'Authorization': '741f24cf76d772b15dcdd896d6044812',
            'Content-Type': 'application/json',
        }

respuesta = requests.post(url_microservicio, headers=headers)
print("=" * 50)
print("Test de llamados al microservicio authentication_service para un usuario Freemium")
print(f"Respuesta del microservicio: {respuesta.text}")
print("=" * 50)

# Test con un usuario no registrado
headers = {
            'Authorization': '741f24cf76d772b15dcdd896d6044812yyy',
            'Content-Type': 'application/json',
        }

respuesta = requests.post(url_microservicio, headers=headers)
print("=" * 50)
print("Test de llamados al microservicio authentication_service para un usuario no registrado")
print(f"Respuesta del microservicio: {respuesta.text}")
print("=" * 50)


# TEST DEL microservicio user_service
# URL del microservicio user_service
url_microservicio = "http://127.0.0.1:5000/user_service"

# Test con un usuario Premium
headers = {
            'Authorization': '7803f9b4f94ab605f48087da2c2a1627',
            'Content-Type': 'application/json',
        }

# Cargar los primeros 10 datos del archivo datos_generados.json

with open("datos_generados_con_errores.json", "r") as archivo:
    datos = json.load(archivo)

print("=" * 50)
print("Test de llamados al microservicio user_service con con parámetros faltantes y con datos fuera de rango")
for dato in datos:
    respuesta = requests.post(url_microservicio, json=dato, headers=headers)

    # Imprimir la respuesta del microservicio
    print(f"Solicitud POST enviada para el dato: {dato}")
    print(f"Respuesta del microservicio: {respuesta.text}")
    print("=" * 50)

print("Todas las solicitudes POST han sido enviadas.")


# Cargar los primeros 10 datos del archivo datos_generados.json
with open("datos_generados.json", "r") as archivo:
    datos = json.load(archivo)[:10]



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
  # Agregar un retardo de 59 segundos después del llamado número 6
    if i == 6:
        print("Esperando 59 segundos...")
        time.sleep(59)

print("Todas las solicitudes POST han sido enviadas.")


# Cargar los primeros 60 datos del archivo JSON
with open("datos_generados.json", "r") as archivo:
    datos = json.load(archivo)[:60]

# URL del microservicio user_service
url_microservicio = "http://127.0.0.1:5000/user_service"

# Test con un usuario Premium
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
        print("Esperando 59 segundos...")
        time.sleep(59)

print("Todas las solicitudes POST han sido enviadas.")


# Cargar los datos del archivo JSON
with open("datos_generados.json", "r") as archivo:
    datos = json.load(archivo)

# URL del microservicio user_service
url_microservicio = "http://127.0.0.1:5002/prediction_service"


# Enviar cada dato como una solicitud POST al microservicio
print("=" * 50)
print("Test de 100 llamados al microservicio prediction_service")
for dato in (datos):
    respuesta = requests.post(url_microservicio, data=dato)

    # Imprimir la respuesta del microservicio
    print(f"Solicitud POST enviada para el dato: {dato}")
    print(f"Respuesta del microservicio: {respuesta.text}")
    print("=" * 50)

print("Todas las solicitudes POST han sido enviadas.")

# Cargar los datos del archivo "datos_generados_log" JSON
with open("datos_generados_log.json", "r") as archivo:
    datos = json.load(archivo)

# URL del microservicio user_service
url_microservicio = "http://127.0.0.1:5003/log_service"



# Enviar cada dato como una solicitud POST al microservicio
print("=" * 50)
print("Test de 100 llamados al microservicio log_service")
for dato in (datos):
    respuesta = requests.post(url_microservicio, data=dato)

    # Imprimir la respuesta del microservicio
    print(f"Solicitud POST enviada para el dato: {dato}")
    print(f"Respuesta del microservicio: {respuesta.text}")
    print("=" * 50)

print("Todas las solicitudes POST han sido enviadas.")
