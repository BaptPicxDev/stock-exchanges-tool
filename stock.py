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
	def showVolumes(self) :
		print("Showing the volume : {}.".format(self.getStockName()))
		if(not self.getDF().empty) :
			df = self.getDF()
			x = df['id']
			y = df['5. volume']
			ticks_range = np.arange(0, df.shape[0], 5)
			
			plt.figure(figsize=(19, 11))
			plt.title("Representation of {} volume evolution the {}.".format(self.getStockName(),  self.getDate()))
			plt.xticks(ticks_range, df['time'][ticks_range], rotation='vertical')
			plt.xlabel("Time")
			plt.ylabel("Volume")
			sns.lineplot(x=x, y=y, markers=True, dashes=False)
			plt.show()

	def show(self, buy_sell_pts=False, labels=True, curve_fiting=False, interpolation=False, max_min=False, sockets=True, meanTrend=True) :
		print("Showing the stock : {}.".format(self.getStockName()))
		if(not self.getDF().empty) :
			df = self.getDF()
			x = df['id']
			y = df['4. close']
			ticks_range = np.arange(0, df.shape[0], 5)

			last = df['4. close'].iloc[-1]
			mean = df['4. close'].mean() 
			high = df['2. high'].max()
			low = df['3. low'].min()
			
			plt.figure(figsize=(19, 11))
			plt.title("Representation of {} stocks evolution the {}.".format(self.getStockName(),  self.getDate()))
			plt.xticks(ticks_range, df['time'][ticks_range], rotation='vertical')
			plt.xlabel("Time")
			plt.ylabel("Stock price")
			plt.ylim((low-1, high+1))
			sns.lineplot(x=x, y=y, markers=True, dashes=False)
			if(curve_fiting) :
				predict_x, predict_y, coefs = getCurvePolyFit(x, y, degree=15)
				sns.lineplot(x=predict_x, y=predict_y, markers=True, dashes=False) # Curve fitting
			if(interpolation) :
				interp_x, interp_y = getCurveInterp(x, y)
				sns.lineplot(x=interp_x, y=interp_y, markers=True, dashes=False) # Curve interpolation 
			if(buy_sell_pts == True) :
				x_b = self.getAccount().getBuyingIds() 
				y_b = [float(df[df['id'] == item]['4. close'].values) for item in x_b]
				x_s = self.getAccount().getSellingIds()
				y_s = [float(df[df['id'] == item]['4. close'].values)  for item in x_s]
				plt.plot(x_b, y_b, 'rx') # plot buy points
				plt.plot(x_s, y_s, 'gx') # plot sell points 
			if(labels) :
				plt.text(x.iloc[-1] + 3, last, 'Last : '+str(last)) # Last  
				plt.text(x.iloc[-1] + 3, low, 'Lowest : '+str(low)) # Lowest
				plt.text(x.iloc[-1] + 3, high, 'Highest : '+str(high)) #  Highest 
				plt.text(x.iloc[-1] + 3, mean - 0.2, 'Mean : '+str(mean)) # Mean
			if(max_min) :
				max_x, max_y = localMaximas(x, y, n_pts=1)
				min_x, min_y = localMinimas(x, y, n_pts=1)
				plt.plot(max_x, max_y, 'ro') # plot the local maximums 
				plt.plot(min_x, min_y, 'bo') # plot the local minimums
			if(sockets) :
				x, mi, ma = getSockets(df)
				# low = self.getLowSocket()
				# high = self.getHighSocket()
				sns.lineplot(x=x, y=mi, markers=True, dashes=False) 
				sns.lineplot(x=x, y=ma, markers=True, dashes=False)
			if(meanTrend) :
				mean_x, mean_y = meanTrend(df)
				sns.lineplot(x=mean_x, y=mean_y)
			# sns.lineplot(x=x, y=low) # Lowest 
			# sns.lineplot(x=x, y=high) # Highest 
			# sns.lineplot(x=x, y=mean) # Mean  
			plt.show()
		else :
			print("Can't draw the figure.")

	# Other function
	def buyStrategy(self, sell_threshold=0.002) :
		print("Trying to buy some "+self.getStockName()+" stocks.")
		df = self.getDF()
		x = df['id'].values
		y = df['4. close'].values
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
				max_x, max_y = localMaximas(x[r], y[r])
				min_x, min_y = localMinimas(x[r], y[r])
				if(buy_flag==True) : # If the buying_flag is set to True.
					if(previous_item<item['4. close']): # Ascending curve.
						if(min_y.size!=0 and (max_y.size==0 or max_x[-1]<min_x[-1])) : # The last local min/max is a minimum.
							if(buyLimit(time=item['time'])) : # If the last time to buy isn't overtaken.
								if(item['4. close'] < y[r].mean() and item['4. close'] <= self.getDayAgo()['close']) : # filter
									self.getAccount().buy(item)
									buy_flag = False
				elif(buy_flag==False) :
					if(previous_item>item['4. close']) : # Descending curve and self.getLastBuyingPrice()!=None 
						if(max_y.size!=0 and (min_y.size==0 or max_x[-1]>min_x[-1])) : # The last local min/max is a maximum 
							if(self.getAccount().checkStock()) : # We have something to sell and the buying_flag is set to False 
								if(item['4. close'] >= (1 + sell_threshold) * self.getAccount().getLastBuyingPrice()) : 
									self.getAccount().sell(item)
									buy_flag = True
				previous_item = item['4. close']

	# Test function
	def test(self) :
		print("Test on the stock : {}.".format(self.getStockName()))
		self.getTrend()





				

	