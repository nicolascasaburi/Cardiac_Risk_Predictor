import os
import sys
import pymongo
from pymongo import errors

####################### SOCKETS ##############################

gateway_service_socket = {"ip":"localhost","port":"5000"}
authentication_service_socket = {"ip":"localhost","port":"5001"}
prediction_service_socket = {"ip":"localhost","port": "5002"}
log_service_socket = {"ip":"localhost","port": "5003"}

##############################################################

#################### DB CONNECTION ###########################

db_connection_string = "mongodb://mongoadmin:secret@localhost"

##############################################################

def main():
    """Start the application"""
    
    load_db()
    start_services()

def load_db():
    """Populate the database with users if they don't exist already"""
    
    try:
        dbClient = pymongo.MongoClient(db_connection_string)
        dbClient.list_databases()        
        db = dbClient['cardiac_risk']
        usuarios = [
                    {'key': '741f24cf76d772b15dcdd896d6044812', 'type': 'freemium'},
                    {'key': '7803f9b4f94ab605f48087da2c2a1627', 'type': 'premium'},
                    {'key': '2ed4bbc82dd29faeb4487092bdc535ed', 'type': 'freemium'},
                    {'key': '61ca6ffc6b94545a58a75ce0637ebf36', 'type': 'premium'},
                    {'key': '33d253c53e5739e7024a4f25abc81b22', 'type': 'freemium'},
                    {'key': 'fb2f370aa9053ca5bb107d888180f94a', 'type': 'premium'},
        ]
        for user in usuarios:
            result = db['users'].find_one(user)
            if result is None:
                db['users'].insert_one(user)
    except errors.ServerSelectionTimeoutError as e:
        print(f"An error occurred while connecting to the MongoDB server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error related to MongoDB has ocurred: {e}") 

def start_services():
    """Start all services with defined ports"""

    # Authentication service
    command = "cd microservices/authentication_service; . .venv/bin/activate; flask --app 'authentication_service:create_app(\""+db_connection_string+"\")' run --port "+authentication_service_socket["port"]+" &"
    os.system(command)

    # Prediction service
    command = "cd microservices/prediction_service; . .venv/bin/activate; flask --app prediction_service.py run --port "+prediction_service_socket["port"]+" &"
    os.system(command)

    # Log service
    command = "cd microservices/log_service; . .venv/bin/activate; flask --app 'log_service:create_app(\""+db_connection_string+"\")' run --port "+log_service_socket["port"]+" &"
    os.system(command)

    # Gateway_service
    command = "cd microservices/gateway_service; . .venv/bin/activate; flask --app 'gateway_service:create_app(\""+authentication_service_socket["ip"]+"\",\""+authentication_service_socket["port"]+"\",\""+prediction_service_socket["ip"]+"\",\""+prediction_service_socket["port"]+"\",\""+log_service_socket["ip"]+"\",\""+log_service_socket["port"]+"\")' run --port "+gateway_service_socket["port"]+" &"
    os.system(command)

main()