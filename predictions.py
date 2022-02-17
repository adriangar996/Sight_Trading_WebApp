#Machine Learning Algorithm
import yfinance as yf
#import math # For estimation
import numpy as np # Processing data as arrays
import pandas as pd # Used to create a dataframe that holds all data
from sklearn.preprocessing import MinMaxScaler # Used to scale data
#import tensorflow as tf # Importation of library used for model creation
#from tensorflow import keras # Importation of backend of tensorflow
#from keras.models import Sequential # Importation of a sequentional model form
#from keras.layers import Dense, LSTM # Importation of Neural Network layers and LSTM layers
from keras.models import load_model # Used to load existing models
import datetime
import joblib
def models_loader(folder, name, days = [1, 5, 30]):
    model = []
    for i in days:
        model.append(load_model(folder+'/'+ name + '_' + str(i) + '.h5'))
    return model

days = [1,5,14,30,90] #Los Dias que el modelo funciona
scaler = joblib.load('scaler.sav')

models = models_loader('ML Model','Model', days) #lodear los modelos 
#Buscar el dia y calcular 75 dias en el pasado
#last = datetime.date.today() 
#td = datetime.timedelta(100)
#start = last - td

companies = ['TSLA', 'AAPL','SIRI','GGB','PLUG']
#print(f'Start: {start}, Last: {last}')

while True:
	time = datetime.datetime.today()
	schedule = datetime.time(17,0,0)
	if time.hour == schedule.hour:
		last = datetime.date.today() 
		td = datetime.timedelta(100)
		start = last - td
		SData = pd.read_csv("http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt", sep='|')
		SData = SData[SData['Test Issue'] == 'N']	
		companies = SData[SData['ETF']=='N']['NASDAQ Symbol'].tolist()
		
		for symbols in companies:
			print(symbols)
			predINV= []
			data = yf.download(symbols,start = start, end = last)
			data = data.filter(['Close'])
			INPUT = data.values
			INPUT = INPUT[-60:]
			scaled_input = scaler.fit_transform(INPUT)
			scaled_input = np.reshape(scaled_input, (-1,60,1))
			for i in range(len(days)):
				pred = models[i].predict(scaled_input) 
				predINV.append(scaler.inverse_transform(pred))
				predINV[i] = predINV[i].round(decimals = 2)
				print(f'Day {days[i]}: {predINV[i]}')
