#####################################
# Developed by Baptiste PICARD      #
# picard.baptiste@laposte.net       #
# Started the 09th of April 2020    #
# picard.baptiste@laposte.net       #
#                                   #
#####################################

# Import
# Librairies
import os

# Modules
from stock import Stock
from access import * 
from utils import * 

# Variables 

class Trading :
	# Constructor
	def __init__(self, name, api_key, stocks, money=1000, risk=5, currency='USD', buy_fee=0, sell_fee=0) :
		self.traiding_name = name
		self.api_key = api_key
		self.currency = currency
		self.my_money = money
		self.risk = risk
		self.stock_names = stocks
		self.stocks = [Stock(s, api_key, './data/'+name+'_'+str(index)+'.json', self.getMoney()/len(self.getStockNames())) for index, s in enumerate(stocks)]
		print("Trading class : {} created.".format(self.getTradingName()))

	# Getters / Setters
	def getTradingName(self) : # Get the name of the instance class (string)
		return self.traiding_name

	def getAPI(self) : # Get the API key (string)
		return self.api_key

	def getCurrency(self) : # Get the currency (string)
		return self.currency

	def getRisk(self) : # Get the risk (integer)
		return self.risk

	def getMoney(self) : # Get the actual ammount of money (integer / float)
		return self.my_money

	def getStockNames(self) :
		return self.stock_names

	def getStocks(self) :
		return self.stocks

	# Functions
	def update(self) : 
		for stock in self.getStocks():
			stock.update()

	def show(self) : 
		for stock in self.getStocks():
			stock.show(curve_fiting=False, buy_sell_pts=True, sockets=True, meanTrend=False, volumes=False)

	def buy(self) : 
		for stock in self.getStocks():
			stock.buyStrategy()

	def test(self) :
		for stock in self.getStocks():
			stock.test()