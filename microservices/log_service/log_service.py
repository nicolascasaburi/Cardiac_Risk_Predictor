import pymongo
from pymongo import errors
import datetime
import time
from flask import (
    Flask,
    request,
    abort,
    g
)  # import flask library

def create_app(db_connection_string,test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    @app.route('/log_service',methods = ['POST'])
    def log_service():
        """Microservice that logs an user request into the database"""

        # Parameters are retrieved from JSON format
        json_data = request.get_json()
        key = json_data.get("key")
        colesterol_level = json_data.get('colesterol_level')
        blood_presure = json_data.get("blood_presure")
        blood_sugar = json_data.get("blood_sugar")
        age = json_data.get("age")
        overweight = json_data.get("overweight")
        smoking = json_data.get("smoking")
        result = json_data.get("result")
        cardiac_risk_index = json_data.get("cardiac_risk_index")
        processing_time = json_data.get("processing_time")
        date = json_data.get("date")

        # Data validation
        error = user_data_validation(key,colesterol_level,blood_presure,blood_sugar,age,overweight,smoking,result,cardiac_risk_index,processing_time,date)
        if error != '':
            abort(404, error)

        # Logging into the bitacora
        error = log(db_connection_string,key,colesterol_level,blood_presure,blood_sugar,age,overweight,smoking,str(float(result)),cardiac_risk_index,processing_time,date)
        if error != '':
            abort(502, error)

        return "The request has been stored in the database successfully"
    return app

def get_db(db_connection_string):
    """This function establishes the connection with the database"""
    
    if 'db' not in g:
        try:
            dbClient = pymongo.MongoClient(db_connection_string)
            db = dbClient['cardiac_risk']
            coll = db['bitacora']
            g.db= coll
        except errors.ServerSelectionTimeoutError as e:
            print(f"An error occurred while connecting to the MongoDB server: {e}")
        except Exception as e:
            print(f"An error related to MongoDB has ocurred: {e}")
    return g.db

def log(db_connection_string:str, key:str, colesterol_level:str, blood_presure:str, blood_sugar:str, age:str, overweight:str, smoking:str, result:str, cardiac_risk_index:str, proccesing_time:time, date:datetime):
    """This functions logs the user request into the bitacora"""

    record = { "key" : key, "colesterol_level" : colesterol_level, "blood_presure" : blood_presure, "blood_sugar" : blood_sugar, "age" : age, "overweight" : overweight, "smoking" : smoking, "result" : result, "cardiac_risk_index" : cardiac_risk_index, "proccesing_time" : proccesing_time, "date" : date }
    try:
        get_db(db_connection_string).insert_one(record)
    except Exception as e:
        return("An error has occurred when logging the request into the bitacora: ", e)
    
    return ''

def user_data_validation(key, colesterol_level, blood_presure, blood_sugar, age, overweight, smoking, result, cardiac_risk_index, processing_time, date):
    """This function verifies that all user parameters exist"""
    error = ''

    # Parameter existence validations
    if key is None:
        error = error + 'key '
    if colesterol_level is None:
        error = error + 'colesterol_level '
    if blood_presure is None:
        error = error + 'blood_presure '
    if blood_sugar is None:
        error = error + 'blood_sugar '
    if age is None:
        error = error + 'age '
    if overweight is None:
        error = error + 'overweight '
    if smoking is None:
        error = error + 'smoking '
    if result is None:
        error = error + 'result '
    if cardiac_risk_index is None:
        error = error + 'cardiac_risk_index '
    if processing_time is None:
        error = error + 'processing_time '
    if date is None:
        error = error + 'date '
    if error != '':
        error = "The following parameters are missing: " + error
        return error

    return error