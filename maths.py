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
from sklearn.linear_model import LinearRegression, RANSACRegressor

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
	m = (pts_y[1] - pts_y[0])/(pts_x[1] - pts_x[0])
	b = pts_y[0] - m * pts_x[0] 
	return m, b # equation  of an equation, degree 1 : y = a*x + b


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
	mean_x, mean_y = df['id'].values.tolist(), [] 
	for index, item in enumerate(y) :
		if(index == 0) :
			mean_y.append(item)
		else : 
			r = np.arange(0, index+1, 1)
			mean_y.append(y[r].mean())
	return mean_x, mean_y

def socketTrends(df, space_separation=6) :
	if(df.shape[0]<space_separation) :
		return np.array([]), np.array([]), 0, 0
	else : 
		minis, maxis, start = [], [], 0
		for i_range in range(int(df.shape[0]/4), df.shape[0], int(df.shape[0]/space_separation)) :
			r = np.arange(start, i_range, 1)
			min_x, min_y = localMinimas(df['id'][r].values, df['4. close'][r].values, n_pts=1)
			max_x, max_y = localMaximas(df['id'][r].values, df['4. close'][r].values, n_pts=1)
			mini, maxi = [(min_x[i], m) for i, m in enumerate(min_y)], [(max_x[i], m) for i, m in enumerate(max_y)]
			items_min = sorted(mini, key=itemgetter(1))
			items_max = sorted(maxi, key=itemgetter(1), reverse=True)
			if(len(items_min)>0) : 
				minis.append(items_min[0])
			if(len(items_max)>0) : 
				maxis.append(items_max[0]) 
			start = i_range
		select_min = sorted(minis, key=itemgetter(1))
		select_max = sorted(maxis, key=itemgetter(1), reverse=True)
		min_x, min_y = [i[0] for i in select_min], [i[1] for i in select_min]
		max_x, max_y = [i[0] for i in select_max], [i[1] for i in select_max]
		min_x, min_y = np.array(min_x), np.array(min_y)
		max_x, max_y = np.array(max_x), np.array(max_y)
		if(len(select_min) >= 2) :
			lr_min = LinearRegression()
			lr_min.fit(min_x.reshape(-1, 1), min_y.reshape(-1, 1))
			new_values_y_min = lr_min.predict(df['id'].values.reshape(-1, 1))
		else :
			new_values_y_min, lr_min = np.array([]), 0

		if(len(select_max) >+ 2) :
			lr_max = LinearRegression()
			lr_max.fit(max_x.reshape(-1, 1), max_y.reshape(-1, 1))
			new_values_y_max = lr_max.predict(df['id'].values.reshape(-1, 1))
		else : 
			new_values_y_max, lr_max = np.array([]), 0
		return new_values_y_min, new_values_y_max, lr_min, lr_max


# Predictions
def getPredictionsLogisticRegression(df) :
	valeus = []
	return values