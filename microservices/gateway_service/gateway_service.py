import datetime
import time
import requests
from bs4 import BeautifulSoup
from flask import (
    Flask,
    request,
    abort,
    jsonify,
)  # import flask library
from requests_cache import CachedSession # import library cache

def create_app(authentication_service_port,prediction_service_port,log_service_port,test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    @app.route('/gateway_service',methods = ['POST'])
    def gateway_service():
        """API Gateway, this gateway interacts with all services as well as the user"""
        
        # Cache initialization
        session = CachedSession('cache_model', backend='sqlite', expire_after=300) # cache expires after 300 seconds
        session.cache.clear()

        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') # turns datetime into a string in order to save it with JSON format
        start_counter = time.time()
        text = []

        # Receive the API Key Authorization
        key = request.headers.get('Authorization')

        # Parameters are retrieved from JSON format
        json_data = request.get_json()
        colesterol_level = json_data.get('colesterol_level')
        blood_presure = json_data.get("blood_presure")
        blood_sugar = json_data.get("blood_sugar")
        age = json_data.get("age")
        overweight = json_data.get("overweight")
        smoking = json_data.get("smoking")         

        # User authentication
        response = requests.post('http://localhost:'+str(authentication_service_port)+'/authentication_service', headers=request.headers)
        if response.status_code != 200:
            message = get_custom_response(response)
            printer(message)
            abort(response.status_code, description = message)

        # Cardiac Risk prediction
        data = {"colesterol_level" : colesterol_level, "blood_presure" : blood_presure, "blood_sugar" : blood_sugar, "age" : age, "overweight" : overweight, "smoking" : smoking}
        response = session.post('http://localhost:'+str(prediction_service_port)+'/prediction_service', json=data)
        if response.status_code != 200:
            message = get_custom_response(response)
            printer(message)
            abort(response.status_code, description = message)
      
        # Format prediction result
        result = response.json()
        text.append("RESULT: " + str(float(result[0])))
        text.append("CARDIAC RISK INDEX: " + result[1])
        
        # Stop counting and calculate the time elapsed for processing
        stop_counter = time.time()
        processing_time = str(stop_counter - start_counter)
        text.append("PROCESSING TIME: " + processing_time + " seconds")
      
        # Log the request into the bitacora
        data = {"key" : key, "colesterol_level" : colesterol_level, "blood_presure" : blood_presure, "blood_sugar" : blood_sugar, "age" : age, "overweight" : overweight, "smoking" : smoking, "result" : str(float(result[0])), "cardiac_risk_index" : result[1], "processing_time" : processing_time, "date" : date }
        response = requests.post('http://localhost:'+str(log_service_port)+'/log_service', json=data)
        if response.status_code != 200:
            message = get_custom_response(response)
            printer(message)
            abort(response.status_code, description = message)
        
        return printer(text)
    return app

def printer(message):
    """Format and print a message in the terminal"""   

    print("\n------------------------------------------------------------------------------------------")
    if type(message) is list:
        for m in message:
            print(m)
    else:
        print(message)
    print("------------------------------------------------------------------------------------------\n")
    return jsonify(message)

def get_custom_response(response) -> str:
    """Get the custom response from an html"""

    soup = BeautifulSoup(response.content, 'html.parser')
    custom_response= soup.find('p').text

    return custom_response