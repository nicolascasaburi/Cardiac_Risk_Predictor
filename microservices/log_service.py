import pymongo
import datetime
import time
import os
from flask import (
    Flask,
    request,
    abort,
    g
)  # se importa la librería principal de flask

def create_app(db_connection_string,test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    @app.route('/log_service',methods = ['POST'])
    def log_service():
        """Microservicio que loguea las solicitudes del usuario"""

        datos_json = request.get_json()
        key = datos_json.get("key")
        nivel_colesterol = datos_json.get('nivel_colesterol')
        presion_arterial = datos_json.get("presion_arterial")
        azucar = datos_json.get("azucar")
        edad = datos_json.get("edad")
        sobrepeso = datos_json.get("sobrepeso")
        tabaquismo = datos_json.get("tabaquismo")         
        resultado = datos_json.get("resultado")
        riesgo_cardiaco = datos_json.get("riesgo_cardiaco")
        tiempo_procesamiento = datos_json.get("tiempo_procesamiento")
        fecha = datos_json.get("fecha")

        # Se valida los datos de entrada
        error = datos_usuario_validos(key,nivel_colesterol,presion_arterial,azucar,edad,sobrepeso,tabaquismo,resultado,riesgo_cardiaco,tiempo_procesamiento,fecha)
        if error != '':
            abort(404, error)

        # Se guarda en la bitacora
        error = logueo(db_connection_string,key,nivel_colesterol,presion_arterial,azucar,edad,sobrepeso,tabaquismo,str(float(resultado)),riesgo_cardiaco,fecha,tiempo_procesamiento)
        if error != '':
            abort(502, error)

        return "La solicitud se registró correctamente en la bitacora"
    return app

def get_db(db_connection_string):
    """Se establece la conexión a la base de datos"""
    
    if 'db' not in g:
        dbClient = pymongo.MongoClient(db_connection_string)
        db = dbClient['riesgo_cardiaco']
        coll = db['bitacora']
        g.db= coll
    return g.db

def logueo(db_connection_string:str, key:str, nivel_colesterol:str, presion_arterial:str, azucar:str, edad:str, sobrepeso:str, tabaquismo:str, resultado:str, riesgo_cardiaco:str, fecha:datetime, tiempo_procesamiento:time):
    """Loguea una solicitud en la bitacora"""

    record = { "key" : key, "nivel_colesterol" : nivel_colesterol, "presion_arterial" : presion_arterial, "azucar" : azucar, "edad" : edad, "sobrepeso" : sobrepeso, "tabaquismo" : tabaquismo, "resultado" : resultado, "riesgo_cardiaco" : riesgo_cardiaco, "fecha" : fecha, "tiempo_procesamiento" : tiempo_procesamiento }
    try:
        get_db(db_connection_string).insert_one(record)
    except Exception as e:
        return("Error al loguear en la bitacora:", e)
    
    return ''

def datos_usuario_validos(key, nivel_colesterol, presion_arterial, azucar, edad, sobrepeso, tabaquismo, resultado, riesgo_cardiaco, tiempo_procesamiento, fecha):
    """Verifica la existencia de los datos del paciente"""
    error = ''

    if key is None:
        error = error + 'key '
    if nivel_colesterol == '':
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
    if resultado is None:
        error = error + 'resultado '
    if riesgo_cardiaco is None:
        error = error + 'riesgo_cardiaco '
    if tiempo_procesamiento is None:
        error = error + 'tiempo_procesamiento '
    if fecha is None:
        error = error + 'fecha '
    if error != '':
        error = "Faltan los parametros: " + error
        return error

    return error