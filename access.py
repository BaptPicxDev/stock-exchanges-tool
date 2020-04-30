#####################################
# Developed by Baptiste PICARD      #
# picard.baptiste@laposte.net       #
# Started the 09th of April 2020    #
# picard.baptiste@laposte.net       #
#                                   #
#####################################

# Librairies
import json
import time
import requests
import datetime as dt

# Modules 
from utils import *

def getTimeSerieDay(item, key, size='full') :
	url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+str(item)+"&outputsize="+size+"&apikey="+str(key)
	while(1) :
		answer = json.loads(requests.get(url).text)
		if('Time Series (Daily)' in answer.keys()) :
			return answer['Time Series (Daily)']

def getTimeSerieWeek(item, key) : 
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+str(item)+'&apikey='+key
	return json.loads(requests.get(url).text)['Weekly Time Series']

def getStockOldValues(item, key) :
	time_serie = getTimeSerieDay(item, key)
	if(time_serie!= None) :
		date_DA = dt.datetime.strptime(getDateDA(), "%Y-%m-%d").date()
		while(str(date_DA) not in time_serie.keys()) :
			date_DA = (date_DA - dt.timedelta(days=1)).strftime('%Y-%m-%d')
			date_DA = dt.datetime.strptime(date_DA, '%Y-%m-%d').date()
		DA = time_serie[str(date_DA)]
		date_WA = dt.datetime.strptime(getDateWA(), "%Y-%m-%d").date()
		while(str(date_WA) not in time_serie.keys()) :
			date_WA = (date_WA -dt.timedelta(days=1)).strftime('%Y-%m-%d')
			date_WA = dt.datetime.strptime(date_WA, '%Y-%m-%d').date()
		WA = time_serie[str(date_WA)]
		date_MA = dt.datetime.strptime(getDateDA(), "%Y-%m-%d").date()
		while(str(date_MA) not in time_serie.keys()) :
			date_MA = (date_MA -dt.timedelta(days=1)).strftime('%Y-%m-%d')
			date_MA = dt.datetime.strptime(date_MA, '%Y-%m-%d').date()
		MA = time_serie[str(date_MA)]
		return DA, date_DA, WA, date_WA, MA, date_MA
	else : 
		return None

def getIntraday(item, key, interval='1min', outputsize="full") : 
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+str(item)+'&interval='+interval+'&outputsize='+outputsize+'&apikey='+key
	cmpt = 0
	while(1) :
		answer = json.loads(requests.get(url).text)
		if('Time Series ('+interval+')' in answer.keys()) :
			return answer['Time Series ('+interval+')']
		else : 
			if(cmpt >=5) :
				print(item + " : Alpha Vantage didn't respond. May check if the symbol exists ")
			print(str(item) + ' : Waiting from >>Alpha Vantage<< to get the data access.')
			time.sleep(10)
			cmpt += 1

def getRateUSDToEUR(key) :
	url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=EUR&apikey="+str(key)
	return json.loads(requests.get(url).text)['Realtime Currency Exchange Rate']['5. Exchange Rate']

def getRateEURToUSD(key) :
	url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey="+str(key)
	return json.loads(requests.get(url).text)['Realtime Currency Exchange Rate']['5. Exchange Rate']
