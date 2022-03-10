import yfinance as yf
#import math # For estimation
import numpy as np # Processing data as arrays
import pandas as pd # Used to create a dataframe that holds all data
#from sklearn.preprocessing import MinMaxScaler # Used to scale data
#import tensorflow as tf # Importation of library used for model creation
#from tensorflow import keras # Importation of backend of tensorflow
#from keras.models import Sequential # Importation of a sequentional model form
#from keras.layers import Dense, LSTM # Importation of Neural Network layers and LSTM layers
from keras.models import load_model # Used to load existing models
import datetime
import joblib

#In order to access Django app DB with standalone python script this section must be included 
import sys, os, django
sys.path.append("/Users/17874/Projects\Capstone_Sight") #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sight.settings")
django.setup()
from Dashboards.models import Predictions


def models_loader(folder, name, days = [1, 5, 30]):
    model = []
    for i in days:
        model.append(load_model(folder+'/'+ name + '_' + str(i) + '.h5'))
    return model
print("Hi")
days = [1,5,14,30,90] #Los Dias que el modelo funciona
scaler = joblib.load('scaler.sav')

models = models_loader('ML Model','Model', days) #lodear los modelos 
#Buscar el dia y calcular 75 dias en el pasado

has_Run = False
companies = ['TSLA', 'AAPL','SIRI','GGB','PLUG', 'GOOG', 'AMZN', 'FB', 'RCL', 'NIO', 'NFLX', 'SNAP']
#print(f'Start: {start}, Last: {last}')

while True:
	#print("Has started")
	time = datetime.datetime.today()
	schedule = datetime.time(21,0,0)
	if time.hour == schedule.hour and has_Run==False: #change second time hour to schedule hour
		last = datetime.date.today() 
		td = datetime.timedelta(100)
		start = last - td
		#SData = pd.read_csv("http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt", sep='|')
		#SData = SData[SData['Test Issue'] == 'N']	
		#companies = SData[SData['ETF']=='N']['NASDAQ Symbol'].tolist()
		
		for symbols in companies:
			print(symbols)
			predINV= []
			data = yf.download(symbols,start = start, end = last)
			data = data.filter(['Close'])
			if len(data.index) > 59:
				INPUT = data.values
				INPUT = INPUT[-60:]
				scaled_input = scaler.fit_transform(INPUT)
				scaled_input = np.reshape(scaled_input, (-1,60,1))
				for i in range(len(days)):
					pred = models[i].predict(scaled_input) 
					predINV.append(scaler.inverse_transform(pred))
					predINV[i] = predINV[i].round(decimals = 2) 
					print(f'Day {days[i]}: {predINV[i]}')
				predINV = np.reshape(predINV,(-1))
				predINV = predINV.tolist()

				#Code to run if Predictions table in DB is empty
				#pred_to_db = Predictions(symbol=symbols, day1=predINV[0],  day5=predINV[1], day14=predINV[2], day30=predINV[3], day90=predINV[4])
				#pred_to_db.save()
				
				#Get all stocks from predictions table in DB
				stocks = Predictions.objects.all()

				#Access all stocks in stocks variable and assign them the new predictions
				for ticker in stocks:
						
					ticker.symbol = symbols
					ticker.day1 = predINV[0]
					ticker.day5 = predINV[1]
					ticker.day14 = predINV[2]
					ticker.day30 = predINV[3]
					ticker.day90 = predINV[4]

				#Save new predictions to DB and add a new stock if any
				ticker.save(update_fields=['symbol', 'day1', 'day5', 'day14', 'day30', 'day90'])

			
			del data 
			has_Run = True	
	
	elif has_Run==True and time.hour != schedule.hour:
		has_Run=False
