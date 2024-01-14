import os

####### PUERTOS #######################

user_service_port = 5000
authentication_service_port = 5001
prediction_service_port = 5002
log_service_port = 5003

#######################################

#################### CONEXION A LA BD ########################

db_connection_string = "mongodb://mongoadmin:secret@localhost"

##############################################################

def main():
    """Inicio de la aplicación"""
    
    cargar_db()
    levantar_servicios()

def cargar_db():
    """Carga la Base de Datos de MongoDB con los usuarios"""
  
    import pymongo
    dbClient = pymongo.MongoClient(db_connection_string)
    db = dbClient['riesgo_cardiaco']
    usuarios = [
    {'key': '741f24cf76d772b15dcdd896d6044812', 'tipo': 'freemium'},
    {'key': '7803f9b4f94ab605f48087da2c2a1627', 'tipo': 'premium'},
    {'key': '2ed4bbc82dd29faeb4487092bdc535ed', 'tipo': 'freemium'},
    {'key': '61ca6ffc6b94545a58a75ce0637ebf36', 'tipo': 'premium'},
    {'key': '33d253c53e5739e7024a4f25abc81b22', 'tipo': 'freemium'},
    {'key': 'fb2f370aa9053ca5bb107d888180f94a', 'tipo': 'premium'},
    ]
    for user in usuarios:
        result = db['usuarios'].find_one(user)
        if result is None:
            db['usuarios'].insert_one(user)

def levantar_servicios():
    """Levanta todos los servicios con los puertos definidos"""

    # Servicio Authentication
    command = "cd microservices; . .venv/bin/activate; flask --app 'authentication_service:create_app(\""+db_connection_string+"\")' run --port "+str(authentication_service_port)+" &"
    os.system(command)

    # Servicio Prediction
    command = "cd microservices; . .venv/bin/activate; flask --app prediction_service.py run --port "+str(prediction_service_port)+" &"
    os.system(command)

    # Servicio Log
    command = "cd microservices; . .venv/bin/activate; flask --app 'log_service:create_app(\""+db_connection_string+"\")' run --port "+str(log_service_port)+" &"
    os.system(command)

    # Servicio User
    command = "cd microservices; . .venv/bin/activate; flask --app 'user_service:create_app("+str(authentication_service_port)+","+str(prediction_service_port)+","+str(log_service_port)+")' run --port "+str(user_service_port)+" &"
    os.system(command)

main()