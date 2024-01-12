#!/usr/bin/env python
# coding: utf-8

# Imports
import numpy as np #Manejar los arreglos con los datos
import pandas as pd #Tomar el dataset y convertir datos categoricos
import matplotlib.pyplot as plt #Para graficar
import pickle
import tensorflow as tf
from tensorflow.keras import models #Crear/entrenar/evaluar el modelo
from tensorflow.keras.layers import Dense, Dropout #Capas densas para la red
from tensorflow.keras.optimizers import Adam #Optimizador a utilizar
from sklearn.model_selection import train_test_split #Para separar train de test
from sklearn.preprocessing import MinMaxScaler #Para normalizar los datos

# Creación del modelo
model = models.Sequential()

# Se agregan las capas
model.add(Dense(50, input_dim=6, activation="relu", kernel_initializer="uniform"))
model.add(Dense(30, activation="relu", kernel_initializer='random_normal'))
model.add(Dense(40, activation="relu", kernel_initializer='random_normal'))
model.add(Dense(1, activation='sigmoid'))

# Se compila el modelo
model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01))
model.summary()

# Se carga el dataset
data = pd.read_csv("datos/datos_de_pacientes.csv")
#data=data.astype(np.float32)

# Se separan los datos de entrada X y los datos de salida Y
X = data.drop(["riesgo_cardiaco"], axis=1)
Y = np.array(data["riesgo_cardiaco"])

# Se quita la primer columna (enumerador)
X = np.array(X.drop(data.columns[0], axis=1))

# Se separan los datos en training y testing
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size= 0.2)

# Se normalizan los datos de entrenamiento y luego los datos de test
scaler = MinMaxScaler()
scaled_X_train = scaler.fit_transform(X_train)
scaled_X_train = pd.DataFrame(scaled_X_train)
scaled_X_test = scaler.fit_transform(X_test)
scaled_X_test = pd.DataFrame(scaled_X_test)

# Se entrena la red
X_train = np.asarray(scaled_X_train).astype(np.float32)
Y_train = np.asarray(Y_train).astype(np.float32)
historial = model.fit(scaled_X_train,Y_train,epochs=20,batch_size=40)

# Se calcula el error
print("----- Cálculo de Loss -----")
test_loss = model.evaluate(scaled_X_test, Y_test)
print(test_loss)

# Se grafica el loss a lo largo de las epocas
plt.xlabel("Número de época")
plt.ylabel("Pérdida/Loss")
plt.plot(historial.history["loss"])

# Se predicen los primeros 3 elementos de entrenamiento
print("----- Predicción de los primeros 3 elementos -----")
print("Datos a predecir:")
print(X_train[:3])
result = model.predict(scaled_X_train[:3])
print("Resultados obtenidos:")
print(result)
print("Valores correctos:")
print(Y_train[:3])

# Se guarda el scaler
scaler_pkl_file = "scaler.pkl"  
with open(scaler_pkl_file, 'wb') as file:  
    pickle.dump(scaler, file)

# Se guarda el modelo
model.save("model.keras")
