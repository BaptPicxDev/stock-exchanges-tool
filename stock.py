#####################################
# Developed by Baptiste PICARD      #
# picard.baptiste@laposte.net       #
# Started the 11th of April 2020    #
# picard.baptiste@laposte.net       #
#                                   #
#####################################

# Imports
# Librairies
import json
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

# Modules 
from account import * 
from access import * 
from utils import * 
from maths import * 

class Stock() :
	# Constructor  
	def __init__(self, name, api_key, json, money) :
		self.stock_name = name
		self.api_key = api_key
		self.json = json
		self.money = money
		self.date = None
		self.day_ago = None
		self.week_ago = None
		self.month_ago = None
		self.df = None
		self.account = Account(name, json)
		self.create()

	# Getters / Setters
	def getStockName(self) :
		return self.stock_name

	def getAPI(self) :
		return self.api_key

	def getJson(self) :
		return self.json

	def getDate(self) :
		return self.date

	def getMoney(self) :
		return self.money

	def getAccount(self) :
		return self.account

	def getDayAgo(self) : # get the different values (day ago) of a stock  (open price, lowest price, highest price, volume, close price : dict)
			return self.day_ago

	def getWeekAgo(self) : # get the different values (day ago) of a stock  (open price, lowest price, highest price, volume, close price : dict)
			return self.week_ago

	def getMonthAgo(self) : # get the different values (day ago) of a stock  (open price, lowest price, highest price, volume, close price : dict)
			return self.day_ago

	def getDF(self) :
		return self.df

	def setDF(self, value) :
		self.df = value

	# Functions 
	# Creation
	def createDates(self) :
		if(self.getDate() == None) :
			self.date = str(dt.datetime.strptime(list(getIntraday(self.getStockName(), self.getAPI()).keys())[0], "%Y-%m-%d %H:%M:%S").date())
		if(self.getDayAgo()==None or self.getMonthAgo()==None or self.getWeekAgo()==None) : 
			DA, dDA, WA, dWA, MA, dMA = getStockOldValues(self.getStockName(), self.getAPI())
			if(DA!=None or WA!=None or MA!=None or dDA!=None or dWA!=None or dMA!=None) :
				self.day_ago = {'date' : dDA, 'open' : float(DA['1. open']), 'close' : float(DA['4. close']), 'high' : float(DA['2. high']), 'low' : float(DA['3. low'])}
				self.week_ago = {'date' : dWA, 'open' : float(WA['1. open']), 'close' : float(WA['4. close']), 'high' : float(WA['2. high']), 'low' : float(WA['3. low'])}
				self.month_ago = {'date' : dMA, 'open' : float(MA['1. open']), 'close' : float(MA['4. close']), 'high' : float(MA['2. high']), 'low' : float(MA['3. low'])}
			print("All dates were created.")
			return 0
		else : 
			return -1 

	def createJson(self) :
		data = {'stock' : self.getStockName(),'buy' : [], 'sell' : [], 'money' : self.getMoney(), 'amount' : 0 }
		if(not os.path.exists(self.getJson())) :
			f = open(self.getJson(),"w")
			json.dump(data, f)
			f.close()
			print('File {} created.'.format(self.getJson()))
		else : 
			json_data = open(self.getJson())
			json_data = json.load(json_data)
			if(json_data.keys() == data.keys()) :
				print('File {} seems to be already exists.'.format(self.getJson()))
			else : 
				return -1

	def create(self) :
		self.createDates()
		self.createJson()			

	# Updating
	def update(self) :
		print("Updating the stock : {} -> {}.".format(self.getStockName(), self.getDate()))
		df = pd.DataFrame(data=getIntraday(self.getStockName(), self.getAPI())).transpose()
		df['day'] = pd.to_datetime(df.index).strftime('%Y-%m-%d')
		df = df[df['day'] == self.getDate()]
		df['time'] = pd.to_datetime(df.index).strftime('%H:%M:%S')
		df = df.astype({'1. open' : 'float64', '2. high' : 'float64', '3. low' : 'float64', '4. close' : 'float64', '5. volume' : 'int'})
		df = df.sort_values(by='time', ascending=True)
		df = df.reset_index(drop=True)
		df['id'] = df.index
		self.setDF(df)

	# Shwoing
	def show(self, buy_sell_pts=False, labels=True, line_labels=False, curve_fiting=False, interpolation=False, max_min=False, sockets=True, meanTrend=True, volumes=False) :
		print("Showing the stock price evolution : {}.".format(self.getStockName()))
		if(not self.getDF().empty) :
			df = self.getDF()
			ticks_range = np.arange(0, df.shape[0], 10)
			plt.figure(figsize=(19, 11))
			plt.title("Representation of {} stocks evolution the {}.".format(self.getStockName(),  self.getDate()))
			plt.xticks(ticks_range, df['time'][ticks_range], rotation='vertical')
			plt.ylim((df['3. low'].min()-1, df['2. high'].max()+1))
			sns.lineplot(x=df['id'], y=df['4. close'], markers=True, dashes=False)
			if(curve_fiting) :
				predict_x, predict_y, coefs = getCurvePolyFit(df['id'], df['4. close'], degree=15)
				sns.lineplot(x=predict_x, y=predict_y, markers=True, dashes=False) # Curve fitting
			if(interpolation) :
				interp_x, interp_y = getCurveInterp(df['id'], df['4. close'])
				sns.lineplot(x=interp_x, y=interp_y, markers=True, dashes=False) # Curve interpolation 
			if(buy_sell_pts == True) :
				x_b, x_s = self.getAccount().getBuyingIds(), self.getAccount().getSellingIds()
				y_b = [float(df[df['id'] == item]['4. close'].values) for item in x_b]
				y_s = [float(df[df['id'] == item]['4. close'].values)  for item in x_s]
				plt.plot(x_b, y_b, 'rx') # plot buy points
				plt.plot(x_s, y_s, 'gx') # plot sell points 
			if(labels) :
				plt.text(df['id'].iloc[-1] + 3, df['4. close'].iloc[-1], 'Last : '+str(df['4. close'].iloc[-1])) # Last
				plt.text(df['id'].iloc[-1] + 3, df['3. low'].min(), 'Lowest : '+str(df['3. low'].min())) # Lowest
				plt.text(df['id'].iloc[-1] + 3, df['2. high'].max(), 'Highest : '+str(df['2. high'].max())) #  Highest
				# plt.text(df['id'].iloc[-1] + 3, df['4. close'].iloc[-1]  - 0.2, 'Mean : '+str(df['4. close'].mean())) # Mean
			if(line_labels) :
				sns.lineplot(x=df['id'], y=df['3. low'].min()) # Lowest
				sns.lineplot(x=df['id'], y=df['2. high'].max()) # Highest
				sns.lineplot(x=df['id'], y=df['4. close'].mean()) # Mean
			if(max_min) :
				max_x, max_y = localMaximas(df['id'], df['4. close'], n_pts=1)
				min_x, min_y = localMinimas(df['id'], df['4. close'], n_pts=1)
				plt.plot(max_x, max_y, 'ro') # plot the local maximums 
				plt.plot(min_x, min_y, 'bo') # plot the local minimums
			if(sockets) :
				mi, ma, _, _ = socketTrends(df)
				if mi.size!= 0:
					sns.lineplot(x=df['id'], y=mi.reshape(1, -1).tolist()[0], markers=True, dashes=False) 
				if ma.size!= 0:
					sns.lineplot(x=df['id'], y=ma.reshape(1, -1).tolist()[0], markers=True, dashes=False)
			if(meanTrend) :
				mean_x, mean_y = meanTrend(df)
				sns.lineplot(x=mean_x, y=mean_y)
			if(volumes) :
				V_std = (df['5. volume'] - df['5. volume'].min()) / (df['5. volume'].max() - df['5. volume'].min()) * 2
				V_scaled = V_std * (df['4. close'].max() - df['4. close'].min()) + df['4. close'].min() - 1
				plt.text(df['id'].iloc[-1] + 3, V_scaled.max(), 'Max Volume : '+str(df['5. volume'].max())) # Last  
				plt.text(df['id'].iloc[-1] + 3, V_scaled.min(), 'Min Volume : '+str(df['5. volume'].min())) # Lowest
				sns.lineplot(x=df['id'], y=V_scaled)
			plt.xlabel("Time")
			plt.ylabel("Stock price")
			plt.show()
		else :
			print("Can't draw the figure.")

	# Other function
	def buyStrategy(self, sell_threshold=0.002) :
		print("Trying to buy some "+self.getStockName()+" stocks.")
		df = self.getDF()
		if(self.getAccount().checkStock()) :
			buy_flag = False
		else :
			buy_flag = True
		previous_item = self.getDF()['1. open'].iloc[0]
		for index_item, item in df.iterrows() :
			if(index_item == 0) :
				pass
			else : 
				r = np.arange(0, index_item+1, 1)
				max_x, max_y = localMaximas(df['id'][r].values, df['4. close'][r].values)
				min_x, min_y = localMinimas(df['id'][r].values, df['4. close'][r].values)
				if(buy_flag==True) : # If the buying_flag is set to True.
					if(previous_item<item['4. close']): # Ascending curve.
						if(min_y.size!=0 and (max_y.size==0 or max_x[-1]<min_x[-1])) : # The last local min/max is a minimum.
							if(buyLimit(time=item['time'])) : # If the last time to buy isn't overtaken.
								new_values_y_min, new_values_y_max, lr_min, lr_max = socketTrends(df.loc[df['id'].isin(r)])
								if(lr_min == 0 or new_values_y_min == np.array([])) : 
									pass
								elif(item['4. close'] <= df.loc[df['id'].isin(r)]['4. close'].quantile(0.25) and item['4. close'] < lr_min.predict(np.array(item['id']).reshape(-1, 1))[0][0]) : # filter
									self.getAccount().buy(item)
									buy_flag = False
				elif(buy_flag==False) :
					if(previous_item>item['4. close']) : # Descending curve and self.getLastBuyingPrice()!=None 
						if(max_y.size!=0 and (min_y.size==0 or max_x[-1]>min_x[-1])) : # The last local min/max is a maximum 
							if(self.getAccount().checkStock()) : # We have something to sell and the buying_flag is set to False 
								new_values_y_min, new_values_y_max, lr_min, lr_max = socketTrends(df.loc[df['id'].isin(r)])
								if(lr_max == 0 or new_values_y_max == np.array([])) : 
									pass
								elif(item['4. close'] >= df.loc[df['id'].isin(r)]['4. close'].quantile(0.75) and item['4. close'] >= self.getAccount().getLastBuyingPrice() and item['4. close'] >= 0.85 * lr_max.predict(np.array(item['id']).reshape(-1, 1))[0][0]) : #filter
									self.getAccount().sell(item)
									buy_flag = True
				previous_item = item['4. close']

	# Test function
	def test(self) :
		print("Test on the stock : {}.".format(self.getStockName()))
		socketTrends(self.getDF())





				

	