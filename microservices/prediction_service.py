from flask import (
    Flask,
    request,
    abort,
)  # se importa la librería principal de flask
from sklearn.preprocessing import MinMaxScaler #Para normalizar los datos
import pandas as pd #Tomar el dataset y convertir datos categoricos
import pickle
import tensorflow as tf
import numpy as np
from bson.json_util import dumps

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    @app.route('/prediction_service',methods = ['POST'])
    def prediction_service():
        """Microservicio que realiza la predicción con el modelo de machine learning"""

        datos_json = request.get_json()
        nivel_colesterol = datos_json.get('nivel_colesterol')
        presion_arterial = datos_json.get("presion_arterial")
        azucar = datos_json.get("azucar")
        edad = datos_json.get("edad")
        sobrepeso = datos_json.get("sobrepeso")
        tabaquismo = datos_json.get("tabaquismo")         

        # Se valida los datos de entrada
        error = datos_usuario_validos(nivel_colesterol,presion_arterial,azucar,edad,sobrepeso,tabaquismo)
        if error != '':
            abort(404, error)

        # Se levanta el modelo ya entrenado
        model = tf.keras.models.load_model("../machine_learning/model.keras")
        
        # Se crea el array con los datos de entrada
        param = np.array([[nivel_colesterol, presion_arterial, azucar, edad, sobrepeso, tabaquismo]]).astype("float32")
        
        # Se obtiene el scaler
        with open('../machine_learning/scaler.pkl', 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)

        # Se normalizan los datos
        scaled_param = scaler.transform(param)
        
        # Se realiza la predicción
        resultado = model.predict(scaled_param,verbose = 0)

        if float(resultado) < 0.50:
            riesgo_cardiaco = "BAJO"
        else:
            riesgo_cardiaco = "ALTO"

        respuesta = [str(float(resultado)), riesgo_cardiaco]

        return respuesta
    
    return app

def datos_usuario_validos(nivel_colesterol, presion_arterial, azucar, edad, sobrepeso, tabaquismo):
    """Verifica que los datos recibidos sean válidos"""
    error = ''

    # Validación de existencia de los datos del paciente
    if nivel_colesterol is None:
        error = error + 'nivel_colesterol '
    if presion_arterial is None:
        error = error + 'presion_arterial '
    if azucar is None:
        error = error + 'azucar '
    if edad is None:
        error = error + 'edad '
    if sobrepeso is None:
        error = error + 'sobrepeso '
    if tabaquismo is None:
        error = error + 'tabaquismo '
    if error != '':
        error = "Faltan los parametros: " + error
        return error

    # Validación del rango de los datos del paciente
    nivel_colesterol = float(nivel_colesterol)
    presion_arterial = float(presion_arterial)
    azucar = float(azucar)
    edad = int(edad)
    sobrepeso = int(sobrepeso)
    tabaquismo = int(tabaquismo)
    if not(nivel_colesterol >= 1.0 and nivel_colesterol <= 3.0):
        error = error + "nivel_colesterol debe ser un valor entre 1.0 y 3.0\n"
    if not(presion_arterial >= 0.6 and presion_arterial <= 1.8):
        error = error + "presion_arterial debe ser un valor entre 0.6 y 1.8\n"
    if not(azucar >= 0.5 and azucar <= 2.0):
        error = error + "azucar debe ser un valor entre 0.5 y 2.0\n"
    if not(edad >= 0 and edad <= 99):
        error = error + "edad debe ser un valor entre 0 y 99\n"
    if not(sobrepeso == 0 or sobrepeso == 1):
        error = error + "sobrepeso debe ser 0 o 1\n"
    if not(tabaquismo == 0 or tabaquismo == 1):
        error = error + "tabaquismo debe ser 0 o 1\n"

    return error