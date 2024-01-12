# Instalación del entorno virtual necesario

## Instalación y despliegue de ambiente para authentication_service

    python3 -m venv .venv

    . .venv/bin/activate
   
    pip install flask
   
    python3 -m pip install "pymongo[svr]"
   
    pip install requests
   
    flask --app authentication_service.py run --port=5001 --debug
   


## Instalación y despliegue de ambiente para prediction_service
   
    python3 -m venv .venv
   
    . .venv/bin/activate
   
    export SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True
   
    pip install sklearn
   
    pip install scikit-learn
   
    pip install pandas
   
    pip install tensorflow
   
    flask --app prediction_service.py run --port=5002 --debug


## Instalación y despliegue de ambiente para log_service

    python3 -m venv .venv
    . .venv/bin/activate
    flask --app log_service.py run --port=5003 --debug


## Instalación y despliegue de ambiente para user_service

    python3 -m venv .venv

    . .venv/bin/activate

    pip install requests_cache

    flask --app 'user_service:create_app(5001,5002,5003)' run --port=5000 --debug



## Instalación de docker-compose

    apt install docker-compose


## Despliegue de contenedor Mongodb

    cd /carpeta contenedora del archivo docker-compose.yml

    docker-compose up -d

# Playground

Corriendo la aplicación Playground.py se pueden testear los microservicios:

    authentication_service
    prediction_service
    log_service
    user_service