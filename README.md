 # Developers

    * Casaburi, Nicolas
    * Casco, Julio

# About
> [!NOTE]
> This software is part of an academic project, and shouldn't be used for real medical porpuses.

Cardiac Risk Predictor is an API developed in Python that predicts cardiac risk based on patient information such as blood pressure, cholesterol level, age, overweight, ect. The provided information is processed by a neural network, which has already been trained with thousands of data from patients records. The machine learning model used by this app was developed with Keras and Tensorflow in order to get an accurate cardiac risk prediction. In addition, this app makes use of a microservice architecture style that is compounded by 4 microservices:
* **gateway service:** the gateway is in charge of the communication among services, working as a central point for managing and coordinating data. Besides, the gateway is the component which interacts with the user.
* **authentication service:** this service is responsible for verifying the identity of users attempting to access the application.
* **prediction service:** this service performs the cardiac risk prediction based on the machine learning model.
* **log service:** the log service registers all user request into the database.
Moreover, a cache is implemented through the requests_cache library in order to speed up the prediction process, decreasing the server load and enhancing the user experience. In terms of persistent data, Cardiac Risk Predictor works with a local Mongo database to save information related to the patient requests. Finally, in order to access to the app, you will need an account key. There are 6 accounts available:

| Key | Account type | Requests per minute |
| --- | --- | --- |
| 741f24cf76d772b15dcdd896d6044812 | freemium | 5 |
| 7803f9b4f94ab605f48087da2c2a1627| premium | 50 |
| 2ed4bbc82dd29faeb4487092bdc535ed| freemium | 5 |
| 61ca6ffc6b94545a58a75ce0637ebf36| premium | 50 |
| 33d253c53e5739e7024a4f25abc81b22| freemium | 5 |
| fb2f370aa9053ca5bb107d888180f94a| premium | 50 |

# Instalation options
## Docker containers (recommended)
This is the recommended option as containers have all required python libraries already installed.
Requirements: docker and docker-compose must be installed in your system before moving to the next step.
1. Cloning this repo:
```
git clone https://github.com/ncasaburi/Cardiac_Risk_Predictor.git
```
2. Move to the app folder whithin the repo:
```
cd Cardiac_Risk_Predictor/docker/app
```
3. Download and run containers:
```
docker-compose up -d
```
The docker-compose.yml placed in the docker/app folder already contains all services required to run this app as well as the database.
Per default, the service ports are assigned as follows:
* gateway service = 5000
* authentication service = 5001
* prediction service = 5002
* log service = 5003
  
The port assignation can be changed as your preference in the docker-compose.yml file.

## Run services manually
Requirements: python3, python3-venv and pip must be installed in your system before moving to the next step. Also, docker and docker-compose will be needed to run the mongo database.
1. Cloning this repo
```
git clone https://github.com/ncasaburi/Cardiac_Risk_Predictor.git
```
2. Move into the repo
```
cd Cardiac_Risk_Predictor/
```
3. Create environment for gateway_service
```
python3 -m venv microservices/gateway_service/.venv; python3 -m venv microservices/authentication_service/.venv; python3 -m venv microservices/prediction_service/.venv; python3 -m venv microservices/log_service/.venv;
```
4. Access to the gateway environment and install the libraries
```
. microservices/gateway_service/.venv/bin/activate; pip install -r microservices/gateway_service/gateway_requirements.txt
```
5. Access to the authentication environment and install the libraries
```
. microservices/authentication_service/.venv/bin/activate; pip install -r microservices/authentication_service/authentication_requirements.txt
```
6. Access to the prediction environment and install the libraries
```
. microservices/prediction_service/.venv/bin/activate; pip install -r microservices/prediction_service/prediction_requirements.txt
```
7. Access to the log environment and install the libraries
```
. microservices/log_service/.venv/bin/activate; pip install -r microservices/log_service/log_requirements.txt
```
8. Move to docker/mongodb
```
cd docker/mongodb
```
9. Run mongo database
```
docker-compose up -d
```
10. Finally, we provide a python script that run all services and populates the database
```
cd  ../../; python3 main.py
```

The ip and port assignation as well as the database connection string can be changed as your preference in the main.py file.

# Tests
We deliver a collection of tests, which are the following:
* Reach limit of request for a Freemium Account
* Reach limit of request for a Premium Account
* Test missing parameters
* Test not authorized account
* Test out of range parameters
* Test services individually
In order to access to these tests, you will need to import the files places in the test folder, and import them into Postman.

# Documentation
As we develop this app, we took several decisions, which were documented describing the context, reasons, benefits and consequences of each. Architectural Desicion Records can be acceded in the ADRs folder.
