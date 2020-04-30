#####################################
# Developed by Baptiste PICARD      #
# picard.baptiste@laposte.net       #
# Started the 09th of April 2020    #
# picard.baptiste@laposte.net       #
# File date creation : 30/04/2020	#
#                                   #
#####################################

# Librairies 
import os 
import json

class Account :
	# Constructor  
	def __init__(self, item, json) :
		self.item = item
		self.json = json 
		self.buying_ids = []
		self.selling_ids = []


	# Getters / Setters 
	def getItem(self) :
		return self.item

	def getJson(self) :
		return self.json

	def getBuyingIds(self) :
		return self.buying_ids

	def addBuyingId(self, _id) :
		self.buying_ids.append(_id)

	def getSellingIds(self) :
		return self.selling_ids

	def addSellingId(self, _id) :
		self.selling_ids.append(_id)

	# Functions 
	def checkStock(self) :
		if(os.path.exists(self.getJson())) :
			json_data = open(self.getJson())
			json_data = json.load(json_data)
			if(json_data['amount']>=1):
				return True
			else : 
				return False 

	def getLastBuyingPrice(self) :
		if(os.path.exists(self.getJson())) :
			json_data = open(self.getJson())
			json_data = json.load(json_data)
			if(len(json_data['buy'])>0) :
				return json_data['buy'][-1]['price']

	def buy(self, item, amount=1) : 
		data = {
					"stock" : self.getItem(),
					"amount" : amount,
					"price" : item['4. close'],
					"time" : item['time']
		}
		if(os.path.exists(self.getJson())) :
			json_data = open(self.getJson())
			json_data = json.load(json_data)
			json_data['buy'].append(data)
			json_data['money'] = json_data['money'] - (item['4. close'] * amount)
			json_data['amount'] += amount
			with open(self.getJson(), "w") as f :
				json.dump(json_data, f)
				f.close()
				self.addBuyingId(item['id'])
				print("Buy {} {} stock at {} -> {}.".format(amount, self.getItem(), item['4. close'], item['time']))

	def sell(self, item, amount=1) : 
		data = {
					"stock" : self.getItem(),
					"amount" : amount,
					"price" : item['4. close'],
					"time" : item['time']
		}
		if(os.path.exists(self.getJson())) :
			json_data = open(self.getJson())
			json_data = json.load(json_data)
			json_data['sell'].append(data)
			json_data['money'] = json_data['money'] + (item['4. close'] * amount)
			if(json_data["amount"]-1 >= 0) :
				json_data['amount'] -= 1
				with open(self.getJson(), "w") as f :
					json.dump(json_data, f)
					f.close()
					self.addSellingId(item['id'])
					print("Sell {} {} stock at {} -> {}.".format(amount, self.getItem(), item['4. close'], item['time']))