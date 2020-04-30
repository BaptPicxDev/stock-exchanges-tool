#####################################
# Developed by Baptiste PICARD      #
# picard.baptiste@laposte.net       #
# Started the 09th of April 2020    #
# picard.baptiste@laposte.net       #
# File date creation : 12/04/2020	#
#                                   #
#####################################

# Import
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
from operator import itemgetter, attrgetter

# Curves
def getCurvePolyFit(x, y, degree=1, step=5) :
	range_values = np.arange(0, len(x), step)
	if(len(x) == len(y)) :
		coefs = np.polyfit(x, y, degree)
		new_x = np.arange(0, len(x), 5)
		new_y = np.polyval(coefs, new_x)
	return new_x, new_y, coefs

def getCurveInterp(x, y, step=5) :
	range_values = np.arange(0, len(x), step)
	if(len(x) == len(y)) :
		new_x = range_values
		new_y = np.interp(range_values, x, y)
	return new_x, new_y, 

def localMaximas(x, y, n_pts=2) :
	if(isinstance(y, pd.core.series.Series)) :
		maximas = argrelextrema(y.to_numpy(), np.greater, order=n_pts)
		return x.iloc[maximas], y.iloc[maximas]
	elif(isinstance(y, np.ndarray)) :
		maximas = argrelextrema(y, np.greater, order=n_pts)
		return x[maximas], y[maximas]

def localMinimas(x, y, n_pts=2) : 
	if(isinstance(y, pd.core.series.Series)) : 
		minimas = argrelextrema(y.to_numpy(), np.less, order=n_pts)
		return x.iloc[minimas], y.iloc[minimas]
	elif(isinstance(y, np.ndarray)) : 
		minimas = argrelextrema(y, np.less, order=n_pts)
		return x[minimas], y[minimas]

def getSockets(df) :
	x = df['id'].values
	y = df['4. close'].values
	min_x, min_y = localMinimas(x, y, n_pts=3)
	max_x, max_y = localMaximas(x, y, n_pts=3)
	minis = []
	maxis = []
	for i, m in enumerate(max_y) :
		maxis.append((max_x[i], m))
	for i, m in enumerate(min_y) :
		minis.append((min_x[i], m))
	minis = sorted(minis, key=itemgetter(1))[0:2]
	maxis = sorted(maxis, key=itemgetter(1), reverse=True)[0:2]
	min_x = [i[0] for i in minis]
	min_y = [i[1] for i in minis]
	max_x = [i[0] for i in maxis]
	max_y = [i[1] for i in maxis]
	print("min : {}".format(min_x))
	print("max : {}".format(min_y))
	return [min_x, min_y], [max_x, max_y]