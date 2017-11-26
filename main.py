from poloniex import poloniex

import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np
import pandas as pd

import time
import datetime

import urllib
import urllib2
import json
import time
import hmac,hashlib

class Conections():

	#Connects with Poloniex
	@staticmethod
	def _connection(username,password):
		conn = poloniex(username,password)
		return conn

	#Conver time format (Ymd to Unix)
	@staticmethod
	def _time_to_unix(date):
		return time.mktime(datetime.datetime.strptime(date, "%Y%m%d").timetuple())

class Trader(Conections):

	def __init__(self,username,password,startTime,endTime):
		self.period = [300, 900, 1800, 7200, 4400, 86400]
		self.pair = "USDT_BTC"
		
		self.startTime 	= Conections._time_to_unix(startTime)
		self.endTime 	= Conections._time_to_unix(endTime)
		
		if username == '' or password == '':
			self.username  	= ''
			self.password	= ''
		else: 
			self.username = username
			self.password = password

		self.conn = Conections._connection(self.username,self.password)

	#Estructure for ticker
	def _set_ticker_list(self,ticker):
		tickerListNames = ['last', 'lowestAsk', 'highestBid', 'percentChange', 'baseVolume', 'quoteVolume', 'isFrozen', '24hrHigh', '24hrLow']
		tickerList = dict()
		tickerList['currencyPair'] = [] 
		for name in tickerListNames:
			tickerList[name] = []

		for name in ticker:
			tickerList['currencyPair'].append(name)
			for label in tickerListNames:
				try:
					tickerList[label].append(ticker[name][label])
				except:
					tickerList[label].append(False)
		return tickerList

	#Returns ticker in DataFrame
	def _get_ticker(self):

		ticker = self.conn.returnTicker()
		tickerList = self._set_ticker_list(ticker)	
		tickerList = pd.DataFrame(tickerList, columns = ['currencyPair','last', 'lowestAsk', 'highestBid', 'percentChange', 'baseVolume', 'quoteVolume', 'isFrozen', '24hrHigh', '24hrLow'] )
		return tickerList

	#Returns pair cotation DataFrame
	def _get_pair_cotation(self):

		historicalData = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period[1]})
		return historicalData
		

	def _plotTest(self):

		N = 500
		random_x = np.linspace(0, 1, N)
		random_y = np.random.randn(N)

		# Create a trace
		trace = go.Scatter(
		    x = random_x,
		    y = random_y
		)

		data = [trace]

		py.iplot(data, filename='basic-line')



trader = Trader('','','20170501','20170531')
trader._get_pair_cotation()