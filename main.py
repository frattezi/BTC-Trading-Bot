import pandas as pd
import numpy as np

import time
import datetime 
import urllib
import urllib2

import json
import hmac,hashlib

from poloniex import poloniex
from candle import Candle

class Trader:

	def __init__(self,username,password,startTime,endTime,period):
		periodList = {'5':300, '15':900, '30':1800, '120':7200, '240':14400, '1440':86400}
		self.period = periodList[period]
		self.pair = "USDT_BTC"
		
		self.startTime = self.TimeToUnix(startTime)
		self.endTime = 	self.TimeToUnix(endTime)

		
		self.username = username
		self.password = password

		self.CandleData = None
		self.candles = [] # CANDLE LIST

		self.conn = self.Connection()

	#Connects with Poloniex
	def Connection(self):
		counter = 0
		while True:		
			try:
				print ('Trying connection')
				conn = poloniex(self.username,self.password)
				return conn
			except:
				wait(1)
				counter += 1
				pass
				if counter == 10:
					print ('fail connection please try again')
					break

	#Get all candles data
	def getCandleHistoricalData(self):
		self.CandleData = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
		self.candles = Candle(self.CandleData)
	
		
	#Convert time format (Ymd to Unix)
	def TimeToUnix(self,date):
		return time.mktime(datetime.datetime.strptime(date, "%Y%m%d").timetuple())

	#Convert time format (Unix to dmY)
	def UnixToTime(self,date):
		return datetime.datetime.utcfromtimestamp(float(date)).strftime('%d-%m-%Y')

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
		ticker = self.conn.returnTicker()
		tickerList = self.setTickerList(ticker)		
		self.tickerList = pd.DataFrame(tickerList, columns = ['currencyPair','last', 'lowestAsk', 'highestBid', 'percentChange', 'baseVolume', 'quoteVolume', 'isFrozen', '24hrHigh', '24hrLow'] )
		print (tickerList)

	def Estrategy(self):
		SimpleAvData = []
		ExpAvData = []
		prevExpAv30 = None
		prevExpAv20	= None
		comprou = 0
		for x in range(0,len(self.candles)):
			#starting average vectors
			if x <	50:
				SimpleAvData.append(self.candles.close(x))
				if x < 30:
					ExpAvData.append(self.candles.close(x))
				else:
					ExpAvData.append(self.candles.close(x))
					ExpAvData.pop(0)
			else:

				SimpleAv = self.MMS(SimpleAvData)
				ExpAvData30, prevExpAv30 = self.MME(ExpAvData,prevExpAv30,30)
				ExpAvData20, prevExpAv20 = self.MME(ExpAvData,prevExpAv20,20)
				
				#Lembrar de colocar para nao comprar novamente nos candles futuros ate ocorrer um ponto de venda
				if SimpleAv > ExpAvData30 and SimpleAv > ExpAvData20 :
					print ('')
					comprou -= self.candles.open(x)

				if SimpleAv < ExpAvData30 and SimpleAv < ExpAvData20 :
					comprou += self.candles.open(x)

		print (comprou)
		print ('e isso ai')


	#Media Movel Simples
	def MMS(self,SimpleAvData):
		return np.average(SimpleAvData)

	#Media Movel Exponencial
	def MME(self,ExpAvData,prevEMA,period):
		multiplier = None
		if prevEMA == None:
			mms = self.MMS(ExpAvData)
			multiplier = (2/(period+1))
			mme = (ExpAvData[len(ExpAvData)-1] - mms)*multiplier+mms
			return mme, mms
		
		else:
			multiplier = (2/(period+1))
			mme = (ExpAvData[len(ExpAvData)-1] - prevEMA)*multiplier+prevEMA
			return mme, prevEMA
		






if __name__ == "__main__":

	startTime = '20171001'
	endTime = '20171101'
	period	= '15'

	trader = Trader('','',startTime,endTime,period)
	trader.Connection()
	#trader.Get_Ticker()
	trader.getCandleHistoricalData()
	trader.Estrategy()
	
