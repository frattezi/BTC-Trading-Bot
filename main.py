from poloniex import poloniex
import time
import pandas as pd
import urllib
import urllib2
import json
import time
import hmac,hashlib

class Trader():

	def __init__(self,username,password):
		self.period = [300, 900, 1800, 7200, 4400, 86400]
		self.pair = "USDT_BTC"
		
		self.startTime = '20160501'
		self.endTime = 	'20170501'
		
		self.username = username
		self.password = password



	#Connects with Poloniex
	def Connection(self):
		conn = poloniex(self.username,self.password)
		return conn

	#Conver time format (Ymd to Unix)
	def TimeToUnix(self,date):
		return time.mktime(datetime.datetime.strptime(date, "%Y%m%d").timetuple())

	#Estructure for ticker
	def setTickerList(self,ticker):
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
	def Get_Ticker(self):
		conn = self.Connection()
			 
		startTime = self.startTime
		endTime = self.endTime

		ticker = conn.returnTicker()
		
		tickerList = self.setTickerList(ticker)
		
		tickerList = pd.DataFrame(tickerList, columns = ['currencyPair','last', 'lowestAsk', 'highestBid', 'percentChange', 'baseVolume', 'quoteVolume', 'isFrozen', '24hrHigh', '24hrLow'] )
		print (tickerList)


		#historicalData = (conn.api_query("returnChartData",{"currencyPair":self.pair,"start":startTime,"end":endTime,"period":self.period[1]}))
		#print (historicalData)




trader = Trader('','')
trader.Get_Ticker()