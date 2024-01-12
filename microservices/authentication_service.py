import pymongo
from datetime import datetime, timedelta
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
    @app.route('/authentication_service',methods = ['POST'])
    def authentication_request():
        """Microservicio que autoriza al usuario"""

        key = request.headers.get('Authorization')
        error = ''

        # Validación de usuario autorizado
        tipo = usuario_registrado(key)
        if not tipo:
            error = 'El usuario no está registrado'
        
        # Validación de la cantidad de solicitudes por minuto
        if alcanzo_maximo(key,tipo):
            error = 'El usuario con cuenta '+tipo+' alcanzó el máximo de solicitudes por minuto'

        return [error]
    return app

def get_db():
    """Se establece la conexión a la base de datos"""
    
    if 'db' not in g:
        dbClient = pymongo.MongoClient('mongodb://mongoadmin:secret@localhost')
        db = dbClient['riesgo_cardiaco']
        g.db= db
    return g.db

def usuario_registrado(hash:str):
    """Contrasta la key ingresada contra la BD"""
    
    result = get_db()['usuarios'].find_one({'key': hash})
    if result:
        return result["tipo"]
    else:
        return False
    
def alcanzo_maximo(key:str, tipo:str):
    "Verifica que el usuario no exceda la cantidad máxima de solicitudes por minuto"
    
    if tipo == "freemium":
        maximo = 5
    else:
        maximo = 50
    
    one_minute_ago = datetime.now() - timedelta(minutes=1)
    query = {"$and":[{"key": key},{"fecha": {"$gte": str(one_minute_ago)}}]}
    solicitudes = get_db()['bitacora'].count_documents(query)    
    if solicitudes >= maximo:
        return True
    return False
