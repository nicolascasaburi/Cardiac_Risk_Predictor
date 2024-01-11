import datetime
import time
import requests
from flask import (
    Flask,
    request,
    Response,
    abort,
    jsonify,
)  # se importa la librería principal de flask
from requests_cache import CachedSession # se importa la libreria de la cache
import os

def create_app(authentication_service_port,prediction_service_port,log_service_port,test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    @app.route('/user_service',methods = ['POST'])
    def predict_request():
        """Microservicio que interactua con el usuario"""
        
        # Se inicializa la cache
        session = CachedSession('cache_modelo', backend='sqlite')
        session.cache.clear()
        session = CachedSession('cache_modelo', backend='sqlite', expire_after=300) # la cache expira luego de 300 segundos
        
        fecha = datetime.datetime.now()
        start_counter = time.time()
        text = []

        # Se obtienen los datos de entrada - en formato JSON
        key = request.headers.get('Authorization')
        datos_json = request.get_json()
        nivel_colesterol = datos_json.get('nivel_colesterol')
        presion_arterial = datos_json.get("presion_arterial")
        azucar = datos_json.get("azucar")
        edad = datos_json.get("edad")
        sobrepeso = datos_json.get("sobrepeso")
        tabaquismo = datos_json.get("tabaquismo")
                
        # Validación de los datos ingresados
        error = datos_usuario_validos(key,nivel_colesterol,presion_arterial,azucar,edad,sobrepeso,tabaquismo)
        if error == '':
            text.append("Los datos ingresados son validos")
        else:
            text=[error]
            printer(text)
            abort(404, description=error)         

        # Validación de usuario autorizado
        response = requests.post('http://localhost:'+str(authentication_service_port)+'/authentication_service', headers=request.headers)
        if response.status_code != 200:
            error = "Falló la autenticación del usuario"
            text=[error]
            printer(text)
            abort(response.status_code, description=error)
        else:
            error = str(response.json()[0])
            if error != '':
                text=[error]
                printer(text)
                abort(404, description=error)    

        # Predicción del riesgo cardíaco
        data = {"nivel_colesterol" : nivel_colesterol, "presion_arterial" : presion_arterial, "azucar" : azucar, "edad" : edad, "sobrepeso" : sobrepeso, "tabaquismo" : tabaquismo}
        response = session.post('http://localhost:'+str(prediction_service_port)+'/prediction_service', data=data)
        if response.status_code != 200:
            error = "Falló la predicción"
            text=[error]
            printer(text)
            abort(response.status_code, description=error)
        
        resultados = response.json()
        text.append("RESULTADO: " + str(float(resultados[0])))
        text.append("RIESGO CARDIACO: " + resultados[1])
        stop_counter = time.time()
        tiempo_procesamiento = str(stop_counter - start_counter)
        text.append("TIEMPO DE PROCESAMIENTO: " + tiempo_procesamiento + " seg")
      
        # Logueo de la solicitud en la bitácora
        data = {"key" : key, "nivel_colesterol" : nivel_colesterol, "presion_arterial" : presion_arterial, "azucar" : azucar, "edad" : edad, "sobrepeso" : sobrepeso, "tabaquismo" : tabaquismo, "resultado" : str(float(resultados[0])), "riesgo_cardiaco" : resultados[1], "tiempo_procesamiento" : tiempo_procesamiento, "fecha" : fecha }
        response = requests.post('http://localhost:'+str(log_service_port)+'/log_service', data=data)
        if response.status_code != 200:
            error = "Falló el logeuo en la bitacora"
            text=[error]
            printer(text)
            abort(response.status_code, description=error)
        
        return printer(text)
    return app

def datos_usuario_validos(key, nivel_colesterol, presion_arterial, azucar, edad, sobrepeso, tabaquismo):
    """Verifica que los datos ingresados por el usuario sean válidos"""
    error = ''

    # Validación de existencia de header
    if not key:
        error = 'Falta el header Authorization con la API key'
        return error

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

def printer(message):
    """Imprime un mensaje por consola y también lo retorna formateado"""   

    print("\n------------------------------------------------------------------------------------------")
    if type(message) is list:
        for m in message:
            print(m)
    else:
        print(message)
    print("------------------------------------------------------------------------------------------\n")
    return jsonify(message)