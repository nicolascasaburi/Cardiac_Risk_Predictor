import pymongo
from pymongo import errors
from datetime import datetime, timedelta
from flask import (
    Flask,
    request,
    abort,
    g
)  # import flask library

def create_app(db_connection_string,test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    @app.route('/authentication_service',methods = ['POST'])
    def authentication_service():
        """Microservice responsible for verifying the identity of users attempting to access the application"""

        key = request.headers.get('Authorization')

        if not key:
            abort(400, "Authorization header with API key is missing")
        
        # Check user authorization
        type = registered_user(db_connection_string,key)
        if not type:
            abort(403, "The user is not registered")
        
        # Request limit validation
        if request_limit_reached(db_connection_string,key,type):
            abort(429, "The user has reached the max number of requests allowed per minute")

        return ["The user is authorized"]
    return app

def get_db(db_connection_string:str):
    """This function establishes the connection with the database"""
    
    if 'db' not in g:
        try:
            dbClient = pymongo.MongoClient(db_connection_string)
            db = dbClient['cardiac_risk']
            g.db= db
        except errors.ServerSelectionTimeoutError as e:
            print(f"An error occurred while connecting to the MongoDB server: {e}")
        except Exception as e:
            print(f"An error related to MongoDB has ocurred: {e}")
    return g.db

def registered_user(db_connection_string:str,hash:str):
    """This function verifies whether the key provided by the user exists in the database"""
    
    result = get_db(db_connection_string)['users'].find_one({'key': hash})
    if result:
        return result["type"]
    else:
        return False
    
def request_limit_reached(db_connection_string:str, key:str, type:str):
    "This function verifies that the user hasn't reached the max number of requests per minute according to his/her account type"
    
    if type == "freemium":
        max_requests = 5 #freemium account
    else:
        max_requests = 50 #premium account
    
    one_minute_ago = datetime.now() - timedelta(minutes=1)
    query = {"$and":[{"key": key},{"date": {"$gte": str(one_minute_ago)}}]}
    user_requests = get_db(db_connection_string)['bitacora'].count_documents(query)    
    if user_requests >= max_requests:
        return True
    return False
