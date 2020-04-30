#####################################
# Developed by Baptiste PICARD      #
# picard.baptiste@laposte.net       #
# Started the 09th of April 2020    #
# picard.baptiste@laposte.net       #
# File date creation : 12/04/2020	#
#                                   #
# This file provides different 		#
# trends, which helps me to get 	#
# information from the price 		#
# evolution.						#
# These functions are used in the 	# 
# function "show" of the stock		#
# class.							#
#####################################

# Import
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
from operator import itemgetter, attrgetter

# Min and Max 
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

# Curves
def get1DLine(pts_x, pts_y) :
	# equation  of an equation, degree 1 : y = a*x + b
	m = (pts_y[1] - pts_y[0])/(pts_x[1] - pts_x[0])
	b = pts_y[0] - m * pts_x[0] 
	return m, b


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
	return new_x, new_y

# Trends
def meanTrend(df) :
	mean_x = df['id'].values.tolist()
	mean_y = []
	for index, item in enumerate(y) :
		if(index == 0) :
			mean_y.append(item)
		else : 
			r = np.arange(0, index+1, 1)
			mean_y.append(y[r].mean())
	return mean_x, mean_y

def getSockets(df) :
	min_x, min_y = localMinimas(df['id'].values, df['4. close'].values, n_pts=3)
	max_x, max_y = localMaximas(df['id'].values, df['4. close'].values, n_pts=3)
	minis, maxis = [(min_x[i], m) for i, m in enumerate(min_y)], [(max_x[i], m) for i, m in enumerate(max_y)]
	minis = sorted(minis, key=itemgetter(1))[0:2]
	maxis = sorted(maxis, key=itemgetter(1), reverse=True)[0:2]
	min_x, min_y = [i[0] for i in minis], [i[1] for i in minis]
	max_x, max_y = [i[0] for i in maxis], [i[1] for i in maxis]
	min_m, min_b = get1DLine(min_x, min_y)
	max_m, max_b = get1DLine(max_x, max_y)
	new_values_y_min = min_m * df['id'].values + min_b
	new_values_y_max = max_m * df['id'].values + max_b
	return df['id'].values, new_values_y_min, new_values_y_max