from flask import (
    Flask,
    request,
    abort,
)  # import flask library
import pickle
import tensorflow as tf
import numpy as np

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    @app.route('/prediction_service',methods = ['POST'])
    def prediction_service():
        """Microservice that performs the cardiac risk prediction based on the machine learning model"""

        # Parameters are retrieved from JSON format
        json_data = request.get_json()
        colesterol_level = json_data.get('colesterol_level')
        blood_presure = json_data.get("blood_presure")
        blood_sugar = json_data.get("blood_sugar")
        age = json_data.get("age")
        overweight = json_data.get("overweight")
        smoking = json_data.get("smoking")               

        # Data validation
        error = user_data_validation(colesterol_level,blood_presure,blood_sugar,age,overweight,smoking)
        if error != '':
            abort(404, error)

        # The previously trained model is loaded
        model = tf.keras.models.load_model("model.keras")
        
        # An array with the user data is created
        param = np.array([[colesterol_level, blood_presure, blood_sugar, age, overweight, smoking]]).astype("float32")
        
        # The scaler is loaded
        with open('scaler.pkl', 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)

        # The data is normalized
        scaled_param = scaler.transform(param)
        
        # Prediction of the cardiac risk using the model
        result = model.predict(scaled_param,verbose = 0)

        if float(result) < 0.50:
            cardiac_risk_index = "LOW"
        else:
            cardiac_risk_index = "HIGH"

        final_result = [str(float(result)), cardiac_risk_index]

        return final_result
    
    return app

def user_data_validation(colesterol_level, blood_presure, blood_sugar, age, overweight, smoking):
    """This function verifies that the user data is correct"""
    error = ''

    # Parameter existence validations
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
    if error != '':
        error = "The following parameters are missing: " + error
        return error

    # Parameter range validations
    colesterol_level = float(colesterol_level)
    blood_presure = float(blood_presure)
    blood_sugar = float(blood_sugar)
    age = int(age)
    overweight = int(overweight)
    smoking = int(smoking)
    if not(colesterol_level >= 1.0 and colesterol_level <= 3.0):
        error = error + "colesterol_level must be between 1.0 and 3.0\n"
    if not(blood_presure >= 0.6 and blood_presure <= 1.8):
        error = error + "blood_presure must be between 0.6 and 1.8\n"
    if not(blood_sugar >= 0.5 and blood_sugar <= 2.0):
        error = error + "blood_sugar must be between 0.5 y 2.0\n"
    if not(age >= 0 and age <= 99):
        error = error + "age must be between 0 and 99\n"
    if not(overweight == 0 or overweight == 1):
        error = error + "overweight must be either 0 or 1\n"
    if not(smoking == 0 or smoking == 1):
        error = error + "smoking must be either 0 or 1\n"

    return error