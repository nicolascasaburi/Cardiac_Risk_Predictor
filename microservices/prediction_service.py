from flask import (
    Flask,
    request,
    Response,
    abort,
    jsonify,
    current_app,
    g
)  # se importa la librería principal de flask
from sklearn.preprocessing import MinMaxScaler #Para normalizar los datos
import pandas as pd #Tomar el dataset y convertir datos categoricos
import pickle
import tensorflow as tf
import numpy as np
from bson.json_util import dumps

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
#    if __name__ == '__main__':
#        app.run(debug=True, port=5002)

    @app.route('/prediction_service',methods = ['POST'])
    def authentication_request():
        """Microservicio que realiza la predicción con el modelo de machine learning"""

        nivel_colesterol = request.form.get("nivel_colesterol")
        presion_arterial = request.form.get("presion_arterial")
        azucar = request.form.get("azucar")
        edad = request.form.get("edad")
        sobrepeso = request.form.get("sobrepeso")
        tabaquismo = request.form.get("tabaquismo")

        # Se levanta el modelo ya entrenado
        model = tf.keras.models.load_model("../machine_learning/model.keras")
        
        # Se crea el array con los datos de entrada
        param = np.array([[nivel_colesterol, presion_arterial, azucar, edad, sobrepeso, tabaquismo]]).astype("float32")
        
        # Se obtiene el scaler
        with open('../machine_learning/model.pkl', 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)

        # Se normalizan los datos
        scaled_param = scaler.transform(param)
        
        # Se realiza la predicción
        resultado = model.predict(scaled_param,verbose = 0)

        if float(resultado) <= 0.33:
            riesgo_cardiaco = "BAJO"
        elif float(resultado) > 0.33 and float(resultado) <= 0.66:
            riesgo_cardiaco = "MEDIO"
        else:
            riesgo_cardiaco = "ALTO"

        respuesta = [str(float(resultado)), riesgo_cardiaco]

        return respuesta
    
    return app