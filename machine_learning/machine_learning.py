#!/usr/bin/env python
# coding: utf-8

# Imports
import numpy as np #library to add support for large and multidimensional arryas
import pandas as pd #library for data manipulation, used to convert dataset into categories
import matplotlib.pyplot as plt #useful for elaborating graphs
import pickle #this is used for serializing the Scaler into a file
import tensorflow as tf 
from tensorflow.keras import models #create, train and evaluate a model
from tensorflow.keras.layers import Dense, Dropout #Dense layers
from tensorflow.keras.optimizers import Adam #Optimizer
from sklearn.model_selection import train_test_split #this is used for splitting the trainging data and the test data
from sklearn.preprocessing import MinMaxScaler #this is used for normalizing the data

# Model creation
model = models.Sequential()

# The layers are added into the model
model.add(Dense(50, input_dim=6, activation="relu", kernel_initializer="uniform"))
model.add(Dense(30, activation="relu", kernel_initializer='random_normal'))
model.add(Dense(40, activation="relu", kernel_initializer='random_normal'))
model.add(Dense(1, activation='sigmoid'))

# Model compilation
model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01))
model.summary()

# Loading the dataset
data = pd.read_csv("datos/datos_de_pacientes.csv")

# The input data and output data are segregated
X = data.drop(["riesgo_cardiaco"], axis=1)
Y = np.array(data["riesgo_cardiaco"])

# The first column (enumerator) is removed
X = np.array(X.drop(data.columns[0], axis=1))

# The training data and test data are segregated
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size= 0.2)

# The training data is normalized as well as the test data
scaler = MinMaxScaler()
scaled_X_train = scaler.fit_transform(X_train)
scaled_X_train = pd.DataFrame(scaled_X_train)
scaled_X_test = scaler.fit_transform(X_test)
scaled_X_test = pd.DataFrame(scaled_X_test)

# Training the model
X_train = np.asarray(scaled_X_train).astype(np.float32)
Y_train = np.asarray(Y_train).astype(np.float32)
historial = model.fit(scaled_X_train,Y_train,epochs=20,batch_size=40)

# Error calculation
print("----- Loss calculation -----")
test_loss = model.evaluate(scaled_X_test, Y_test)
print(test_loss)

# Graphing the loss over the epochs
plt.xlabel("Epoch number")
plt.ylabel("Loss")
plt.plot(historial.history["loss"])

# Prediction of the first 3 elements
print("----- Prediction of the first 3 elements -----")
print("Data to predict:")
print(X_train[:3])
result = model.predict(scaled_X_train[:3])
print("Results:")
print(result)
print("Correct values:")
print(Y_train[:3])

# The scaler is saved in a file
scaler_pkl_file = "../microservices/prediction_service/scaler.pkl"  
with open(scaler_pkl_file, 'wb') as file:  
    pickle.dump(scaler, file)

# The model is saved in a file
model.save("../microservices/prediction_service/model.keras")
