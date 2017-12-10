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

from player import Player
from Strategy import BacktestStrategy

class Trader:

	def __init__(self,username,password,startTime,endTime,period):
		periodList = {'5':300, '15':900, '30':1800, '120':7200, '240':14400, '1440':86400}
		self.period = periodList[period]
		self.pair = "USDT_BTC"
		self.onTop = "SimpleMM"


		self.startTime = self.TimeToUnix(startTime)
		self.endTime = 	self.TimeToUnix(endTime)

		
		self.username = username
		self.password = password

		self.CandleData = None
		self.candles = [] # CANDLE LIST

		self.conn = self.Connection()

		self.player1 = Player()
		self.player2 = Player()

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

	#Get all candles data
	def getCandleHistoricalData(self):
		self.CandleData = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
		self.candles = Candle(self.CandleData)
	
	def Get_Ticker(self):
		ticker = self.conn.returnTicker()
		tickerList = self.setTickerList(ticker)		
		self.tickerList = pd.DataFrame(tickerList, columns = ['currencyPair','last', 'lowestAsk', 'highestBid', 'percentChange', 'baseVolume', 'quoteVolume', 'isFrozen', '24hrHigh', '24hrLow'] )
		return self.tickerList

	# OBS :Poderia ter apenas dado pass nos 50 primeiros e usar slicing para controlar as janelas - mais facil
	def Backtest(self):
		strat1 = BacktestStrategy()
		strat2 = BacktestStrategy()
		
		player1 = Player()
		
		SimpleAvData = []
		ExpAvData = []
		
		prevExpAv20	= None
		prevExpAv30 = None
		ExpAvData20 = None
		ExpAvData30 = None
		firstCandle = True
		
		bank = 0
		counter = 0
		
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
				if firstCandle == True:
					PrevSimpleAv20 = None
					PrevSimpleAv50 = None
					firstCandle = False
				else:

					SimpleAvData.append(self.candles.close(x))
					SimpleAvData.pop(0)

					ExpAvData.append(self.candles.close(x))
					ExpAvData.pop(0)



					SimpleAv20,SimpleAv50 = self.MMS(SimpleAvData)
					ExpAvData30, prevExpAv30 = self.MME(ExpAvData30, self.candles.close(x), 30)
					ExpAvData20, prevExpAv20 = self.MME(ExpAvData20, self.candles.close(x), 20)
					
					'''
					Agora abaixo vao as estrategias chamadas da class Strategy, podemos
					instaciar um objeto de class para cada estrategia e ter todos os resultados do 
					backtest ao final da apresentacao
					'''
					if PrevSimpleAv20 == None:
						PrevSimpleAv20 = SimpleAv20
					
					else:
						#strat1.SimpleAVPrice(self.player1,self.candles.CloseDate(x),SimpleAv20,PrevSimpleAv20)
						#strat2.ExpSimpleAv(self.player2,self.candles.CloseDate(x),SimpleAv20)
						self.onTop = strat2.ExpSimpleAv(SimpleAv20, ExpAvData20, ExpAvData30, self.onTop, self.player1, self.candles.CloseDate(x))
					#	strat1.SimpleAVPrice(self.player1,self.candles.CloseDate(x),SimpleAv20,PrevSimpleAv20)
					PrevSimpleAv20 = SimpleAv20

		return player1	

	#Media Movel Simples
	def MMS(self,SimpleAvData):
		#print (len(SimpleAvData))
		return np.average(SimpleAvData),np.average(SimpleAvData[30:])

	#Media Movel Exponencial
	def MME(self, prevEMA, lastCandleValue, period):
		if prevEMA != None:
			mme = ((lastCandleValue * period) + (prevEMA * (100-period)))/100
			new_prevEMA = prevEMA
		else:
			mme = lastCandleValue
			new_prevEMA = mme
		return mme, new_prevEMA




if __name__ == "__main__":

	startTime = '20171110'
	endTime = '20171210'
	period	= '120'
	
	trader = Trader('','',startTime,endTime,period)
	trader.Connection()
	trader.getCandleHistoricalData()
	trader.Backtest()
	tickerlist = trader.Get_Ticker()
	lastprice = (float(tickerlist['last'][20]))

	trader.player1.SowFinalResults(lastprice)		#tickerlist = Last USDT-BTC sell value
	#trader.player2.SowFinalResults(lastprice)