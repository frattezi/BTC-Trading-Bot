from poloniex import poloniex
import time
import pandas as pd
import urllib
import urllib2
import candle
import json
import time
import hmac,hashlib

class Trader:

	def __init__(self,username,password):
		self.period = [300, 900, 1800, 7200, 4400, 86400]
		self.pair = "USDT_BTC"
		
		self.startTime = "1508797168"
		self.endTime = 	"1511475568"
		
		self.username = username
		self.password = password

		self.CandleData = None
		self.candles = [] # CANDLE LIST

	#Connects with Poloniex
	def Connection(self):
		conn = poloniex(self.username,self.password)
		return conn

	def getCandleData(self, conn):
		#Get all candles data
		self.CandleData = conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period[0]})
		self.candles = candle.Candle(self.CandleData)
		
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

	def Get_Ticker(self):
		conn = self.Connection()
		
		self.getCandleData(conn)	 

		startTime = self.startTime
		endTime = self.endTime

		ticker = conn.returnTicker()
		
		tickerList = self.setTickerList(ticker)
		
		tickerList = pd.DataFrame(tickerList, columns = ['currencyPair','last', 'lowestAsk', 'highestBid', 'percentChange', 'baseVolume', 'quoteVolume', 'isFrozen', '24hrHigh', '24hrLow'] )
		print (tickerList)

		#historicalData = (conn.api_query("returnChartData",{"currencyPair":self.pair,"start":startTime,"end":endTime,"period":self.period[1]}))
		#print (historicalData)

	def buyStrategy(self):
		for i in range(0, len(self.candles)):
			if self.candles.open(i) < self.candles.close(i):
				print("Compre")

	def sellStrategy(self):
		for i in range(0, len(self.candles)):
			if self.candles.high(i) > (self.candles.close(i) + 200):
				print("Venda")


trader = Trader('','')
trader.Connection()
trader.Get_Ticker()

#buy and sell orders
trader.buyStrategy()
trader.sellStrategy()