import os

def main():
    """Menú interactivo"""
    
    print("*** EVALUACION DE RIESGO CARDIACO ***")

    while(True):
        print("\nElija una opción y precione enter:")
        option = input("1 - Cargar la Base de Datos MongoDB con los datos\n2 - Levantar los servicios\n3 - Bajar los servicios\n4 - Salir\nrespuesta [1,2,3,4]:")
        print("\n")
        match option:
            case "1": 
                cargar_db()
            case "2":
                levantar_servicios()
            case "3":
                bajar_servicios()
            case "4":
                break
            case _:
                print("debe elegir una opción entre 1 y 4")

def cargar_db():
    """Carga la Base de Datos de MongoDB con los datos"""
  
    import pymongo
    dbClient = pymongo.MongoClient('mongodb://mongoadmin:secret@localhost')
    db = dbClient['riesgo_cardiaco']
    usuarios = [
    {'key': '741f24cf76d772b15dcdd896d6044812', 'tipo': 'freemium'},
    {'key': '7803f9b4f94ab605f48087da2c2a1627', 'tipo': 'premium'},
    {'key': '2ed4bbc82dd29faeb4487092bdc535ed', 'tipo': 'freemium'},
    {'key': '61ca6ffc6b94545a58a75ce0637ebf36', 'tipo': 'premium'},
    {'key': '33d253c53e5739e7024a4f25abc81b22', 'tipo': 'freemium'},
    {'key': 'fb2f370aa9053ca5bb107d888180f94a', 'tipo': 'premium'},
    ]
    db['usuarios'].insert_many(usuarios)

def levantar_servicios():
    """Levanta todos los servicios con los puertos definidos"""

    # Servicio Authentication
    command = "cd microservices; . .venv/bin/activate; flask --app authentication_service.py run --port 5001 &"
    os.system(command)

    # Servicio Prediction
    command = "cd microservices; . .venv/bin/activate; flask --app prediction_service.py run --port 5002 &"
    os.system(command)

    # Servicio Log
    command = "cd microservices; . .venv/bin/activate; flask --app log_service.py run --port 5003 &"
    os.system(command)

    # Servicio User
    command = "cd microservices; . .venv/bin/activate; flask --app 'user_service:create_app(5001,5002,5003)' run --port 5000 &"
    os.system(command)

def bajar_servicios():
    """Baja todos los servicios"""

    command = "killall flask"
    os.system(command)

main()