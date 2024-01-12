# ADR: Diagnóstico de Riesgo Cardíaco

## Contexto

Se requiere desarrollar un servicio web (API) que exponga un modelo de red neuronal para diagnosticar riesgo cardíaco a partir de datos clínicos del paciente. Se establece la necesidad de autenticación mediante API keys y se limita la frecuencia de solicitudes según el tipo de cuenta del cliente. Además, se debe registrar cada solicitud en una bitácora y se sugiere la implementación de caché para datos de solo lectura.

## Decisiones Principales

1. **Desarrollo de Servicios:**
   - Se opta por la arquitectura de microservicios para modularizar y desacoplar las funcionalidades del sistema.

2. **Lenguaje de Programación:**
   - Se decide utilizar Python para la implementación de la aplicación y servicios, dada su eficiencia en procesamiento de datos y amplio soporte para bibliotecas de machine learning.

3. **Framework para los microservicios:**
   - Flask se selecciona como el framework para los microservicios debido a su simplicidad y capacidad para integrarse fácilmente con otras tecnologías.

4. **Contenedorización:**
   - Se utiliza Docker para contener y distribuir la aplicación machine_learning, los microservicios y la base de datos mongo, garantizando la consistencia del entorno de ejecución.

5. **Base de Datos:**
   - MongoDB es la base de datos seleccionada para almacenar información relacionada con usuarios y bitácora, debido a su flexibilidad y escalabilidad.

6. **Modelo de Red Neuronal:**
   - Se elige un modelo secuencial para la red neuronal, que se entrena con datos clínicos para diagnosticar riesgo cardíaco.

7. **Biblioteca para la creación y entrenamiento del Modelo:**
   - Se utiliza la biblioteca Keras para la creación y entrenamiento del modelo, dada su compatibilidad con otras bibliotecas como TensorFlow, su simplicidad y modularidad.

8. **Seguridad:**
   - La autenticación de los servicios se realiza mediante API keys, verificando la existencia de la clave en la base de datos. Además, se implementa un control de límites de solicitudes por minuto según el tipo de cuenta (FREEMIUM o PREMIUM).

9. **Registro en Bitácora:**
   - Se decide registrar cada solicitud en una bitácora, almacenando información relevante como API key, datos clínicos, resultado de la predicción y tiempo de procesamiento.

10. **Caché:**
    - Se implementa un sistema de caché para almacenar datos de solo lectura y reducir la carga en la base de datos.

## ADR: Aplicación machine_learning

1. **Tecnologías:**
   - Se utiliza Python para el desarrollo de la aplicación machine_learning debido a su ligereza y facilidad de integración con otros componentes.

2. **Interfaz de Usuario:**
   - La aplicación machine_learning no tiene una interfaz de usuario directa; genera un archivo modelo que es utilizado por el microservicio prediction_service, el cual es accedido mediante solicitudes HTTP.

3. **Modelo de Red Neuronal:**
   - Se elige un modelo secuencial para la red neuronal, el cual es entrenado con datos clínicos para clasificar el riesgo cardíaco.

4. **Persistencia del Modelo:**
   - El modelo entrenado se guarda en un archivo (model.keras) para su posterior carga y uso.

5. **Funciones Principales:**
   - La aplicación machine_learning se encarga de crear, compilar, entrenar y guardar el modelo. Además, proporciona funciones para cargar el modelo, normalizar datos y realizar predicciones.

## ADR: Microservicio user_service

1. **Funcionalidad:**
   - Actúa como punto de entrada para los usuarios que desean realizar predicciones de riesgo cardíaco. Coordina las acciones entre los microservicios, realiza autenticación y registra solicitudes en la bitácora.

2. **Autenticación:**
   - Verifica la API key mediante el microservicio authentication_service antes de procesar la solicitud.

3. **Solicitud al Modelo:**
   - Hace solicitudes al microservicio prediction_service para obtener la predicción de riesgo cardíaco.

4. **Registro en Bitácora:**
   - Luego de recibir la respuesta, pasa la información al microservicio log_service para su registro en la bitácora.

## ADR: Microservicio authentication_service

1. **Funcionalidad:**
   - Se encarga de autenticar la API key proporcionada en la solicitud del usuario.

2. **Conexión a Base de Datos:**
   - Se conecta a la base de datos MongoDB para verificar la existencia de la API key en la colección de usuarios.

3. **Respuesta:**
   - Devuelve un error si la API key no está registrada, permitiendo el flujo normal si la autenticación es exitosa.

## ADR: Microservicio prediction_service

1. **Funcionalidad:**
   - Recibe datos clínicos, carga el modelo previamente entrenado, normaliza los datos y realiza predicciones de riesgo cardíaco.

2. **Carga del Modelo:**
   - Levanta el modelo entrenado utilizando la libreria de Keras.

3. **Normalización de Datos:**
   - Normaliza los datos clínicos antes de realizar la predicción.

4. **Respuesta:**
   - Devuelve el resultado numérico de la predicción y también un índice del riesgo cardíado (BAJO o ALTO).

## ADR: Microservicio log_service

1. **Funcionalidad:**
   - Recibe información relevante de las solicitudes (API key, datos clínicos, resultado de predicción, tiempo de procesamiento) y la guarda en la base de datos en la colección bitácora.

2. **Conexión a Base de Datos:**
   - Se conecta a la base de datos MongoDB para almacenar la información en la colección bitácora.

3. **Registro de Tiempo:**
   - Registra el tiempo que toma procesar la solicitud HTTP, desde la recepción hasta la respuesta final.

## Conclusiones

La arquitectura propuesta garantiza la modularidad, escalabilidad y seguridad del sistema de diagnóstico de riesgo cardíaco. La implementación de microservicios permite una fácil gestión y actualización de cada componente, y la contenerización facilita la distribución del sistema. La aplicación machine_learning proporciona las funcionalidades clave para el entrenamiento y uso del modelo de red neuronal, mientras que los microservicios coordinan la autenticación, predicción y registro de solicitudes. La utilización de tecnologías como MongoDB, Flask y Docker contribuye a la eficiencia y mantenibilidad del sistema.

