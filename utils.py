#####################################
# Developed by Baptiste PICARD      #
# picard.baptiste@laposte.net       #
# Started the 09th of April 2020    #
# picard.baptiste@laposte.net       #
#                                   #
#####################################

# Import
import os 
import json
import pytz # modify the timezone
import datetime as dt # datetime format 
from copy import copy, deepcopy # copy and deepcopy for lists


# Variables 
US_UTC = pytz.timezone('US/Eastern')
EUR_UTC = pytz.timezone('Europe/Amsterdam')
BUY_LIMIT = 0

# Time 
# Today
def getDatetime(utc_selection=US_UTC) : 
	return dt.datetime.now(utc_selection).strftime('%Y-%m-%d %H:%M:%S')

def getDate(utc_selection=US_UTC) : 
	return dt.datetime.now(utc_selection).strftime('%Y-%m-%d')

def getTime(utc_selection=US_UTC) :
	return dt.datetime.now(utc_selection).strftime('%H:%M:%S')

# Hour comparison
def buyLimit(time=None, utc_selection=US_UTC) :
	if(time==None) : # Compare with the current time
		hours =  int(dt.datetime.now(utc_selection).hour) 
		minutes = int(dt.datetime.now(utc_selection).minute)
	else : 
		hours, minutes, seconds = map(int, time.split(':'))
	current_time = hours*60 + minutes
	limit = 14*60 # 14h
	if(current_time <= limit) :
		return True # Continue to buy ! 
	elif(current_time > limit) :
		return False # Stop buying
		
# Day ago
def getDateDA(utc_selection=US_UTC) : 
	return (dt.datetime.now(utc_selection)-dt.timedelta(days=1)).strftime('%Y-%m-%d')

# Week ago
def getDateWA(utc_selection=US_UTC) : 
	return (dt.datetime.now(utc_selection)-dt.timedelta(weeks=1)).strftime('%Y-%m-%d')

# Month ago
def getDateMA(utc_selection=US_UTC) : 
	return (dt.datetime.now(utc_selection)-dt.timedelta(weeks=3)).strftime('%Y-%m-%d')

# List copies 
def createCopyList(l) :
	return deepcopy(l)
