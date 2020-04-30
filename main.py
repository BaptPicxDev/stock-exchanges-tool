#####################################
# Developed by Baptiste PICARD      #
# picard.baptiste@laposte.net       #
# Started the 09th of April 2020    #
# picard.baptiste@laposte.net       #
#                                   #
#####################################

# Librairies 
import os
import time
import json
import matplotlib.pyplot as plt

# Modules
from access import *
from utils import * 
from trading import *

# Environment
plt.close('all')

# Variables
JSON_FILE = './data/config.json'
OPEN_MARKET = dt.time(9, 0, 0)
CLOSE_MARKET = dt.time(16, 0, 0)

if __name__ == "__main__" :
	start = time.time()
	print("Script starting : {}.".format(getDatetime()))
	my_json = json.load(open(JSON_FILE))
	if(getTime() >= str(OPEN_MARKET) and getTime()<=str(CLOSE_MARKET)) :
		#print("Bourse de NY open")
		pass
	else : 
		#print("Bourse de NY close")
		pass
	Tr = Trading("Trading01", my_json['ALPHA_VANTAGE_API_KEY'], my_json['STOCKS'])
	Tr.update()	
	# Tr.test()
	Tr.buy()
	Tr.show()
	print("End of this script in {} seconds.".format(time.time() - start))
	 