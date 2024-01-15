import sys
import pymongo
from pymongo import errors

def main(db_connection_string):
    """This script is called by docker in order to start the gateway_service container"""

    load_db(db_connection_string)
    
def load_db(db_connection_string):
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

main(sys.argv[1])
