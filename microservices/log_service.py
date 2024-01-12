import pymongo
import datetime
import time
from flask import (
    Flask,
    request,
    Response,
    abort,
    jsonify,
    current_app,
    g
)  # se importa la librería principal de flask

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    @app.route('/log_service',methods = ['POST'])
    def authentication_request():
        """Microservicio que loguea las solicitudes del usuario"""

        key = request.form.get("key")
        nivel_colesterol = request.form.get("nivel_colesterol")
        presion_arterial = request.form.get("presion_arterial")
        azucar = request.form.get("azucar")
        edad = request.form.get("edad")
        sobrepeso = request.form.get("sobrepeso")
        tabaquismo = request.form.get("tabaquismo")
        resultado = request.form.get("resultado")
        riesgo_cardiaco = request.form.get("riesgo_cardiaco")
        tiempo_procesamiento = request.form.get("tiempo_procesamiento")
        fecha = request.form.get("fecha")

        logueo(key,nivel_colesterol,presion_arterial,azucar,edad,sobrepeso,tabaquismo,str(float(resultado)),riesgo_cardiaco,fecha,tiempo_procesamiento)

        return "La solicitud se registró correctamente en la bitacora"
    return app

def get_db():
    """Se establece la conexión a la base de datos"""
    
    if 'db' not in g:
        dbClient = pymongo.MongoClient('mongodb://mongoadmin:secret@localhost')
        db = dbClient['riesgo_cardiaco']
        coll = db['bitacora']
        g.db= coll
    return g.db

def logueo(key:str, nivel_colesterol:str, presion_arterial:str, azucar:str, edad:str, sobrepeso:str, tabaquismo:str, resultado:str, riesgo_cardiaco:str, fecha:datetime, tiempo_procesamiento:time):
    """Loguea una solicitud en la bitacora"""

    record = { "key" : key, "nivel_colesterol" : nivel_colesterol, "presion_arterial" : presion_arterial, "azucar" : azucar, "edad" : edad, "sobrepeso" : sobrepeso, "tabaquismo" : tabaquismo, "resultado" : resultado, "riesgo_cardiaco" : riesgo_cardiaco, "fecha" : fecha, "tiempo_procesamiento" : tiempo_procesamiento }
    get_db().insert_one(record)