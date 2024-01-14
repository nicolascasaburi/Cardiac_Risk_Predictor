import datetime
import time
import requests
from bs4 import BeautifulSoup
from flask import (
    Flask,
    request,
    abort,
    jsonify,
)  # se importa la librería principal de flask
from requests_cache import CachedSession # se importa la libreria de la cache

def create_app(authentication_service_port,prediction_service_port,log_service_port,test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    @app.route('/user_service',methods = ['POST'])
    def user_service():
        """Microservicio que interactua con el usuario"""
        
        # Se inicializa la cache
        session = CachedSession('cache_modelo', backend='sqlite')
        session.cache.clear()
        session = CachedSession('cache_modelo', backend='sqlite', expire_after=300) # la cache expira luego de 300 segundos
        
        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        start_counter = time.time()
        text = []

        # Se obtiene la API Key Authorization
        key = request.headers.get('Authorization')
        # Se obtienen los datos de entrada en formato JSON
        datos_json = request.get_json()
        nivel_colesterol = datos_json.get('nivel_colesterol')
        presion_arterial = datos_json.get("presion_arterial")
        azucar = datos_json.get("azucar")
        edad = datos_json.get("edad")
        sobrepeso = datos_json.get("sobrepeso")
        tabaquismo = datos_json.get("tabaquismo")         

        # Validación de usuario autorizado
        response = requests.post('http://localhost:'+str(authentication_service_port)+'/authentication_service', headers=request.headers)
        if response.status_code != 200:
            message = get_custom_response(response)
            printer(message)
            abort(response.status_code, description = message)

        # Predicción del riesgo cardíaco
        data = {"nivel_colesterol" : nivel_colesterol, "presion_arterial" : presion_arterial, "azucar" : azucar, "edad" : edad, "sobrepeso" : sobrepeso, "tabaquismo" : tabaquismo}
        response = session.post('http://localhost:'+str(prediction_service_port)+'/prediction_service', json=data)
        if response.status_code != 200:
            message = get_custom_response(response)
            printer(message)
            abort(response.status_code, description = message)
      
        resultados = response.json()
        text.append("RESULTADO: " + str(float(resultados[0])))
        text.append("RIESGO CARDIACO: " + resultados[1])
        stop_counter = time.time()
        tiempo_procesamiento = str(stop_counter - start_counter)
        text.append("TIEMPO DE PROCESAMIENTO: " + tiempo_procesamiento + " seg")
      
        # Logueo de la solicitud en la bitácora
        data = {"key" : key, "nivel_colesterol" : nivel_colesterol, "presion_arterial" : presion_arterial, "azucar" : azucar, "edad" : edad, "sobrepeso" : sobrepeso, "tabaquismo" : tabaquismo, "resultado" : str(float(resultados[0])), "riesgo_cardiaco" : resultados[1], "tiempo_procesamiento" : tiempo_procesamiento, "fecha" : fecha }
        response = requests.post('http://localhost:'+str(log_service_port)+'/log_service', json=data)
        if response.status_code != 200:
            message = get_custom_response(response)
            printer(message)
            abort(response.status_code, description = message)
        
        return printer(text)
    return app

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

def get_custom_response(response) -> str:
    """Obtiene el custom response desde una respuesta html"""

    soup = BeautifulSoup(response.content, 'html.parser')
    custom_response= soup.find('p').text

    return custom_response