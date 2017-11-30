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

import player

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

		self.mercador = player.Player()

		self.onTop = None

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

	# OBS :Poderia ter apenas dado pass nos 50 primeiros e usar slicing para controlar as janelas
	def BacktestEstrategy(self):
		SimpleAvData = []
		ExpAvData = []
		prevExpAv30 = None
		prevExpAv20	= None
		firstCandle = True
		firstIteration = True
		ExpAvData30 = None
		ExpAvData20 = None

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
					if counter < 4:
						#print (x)
						#print (SimpleAvData)
						counter+=1
					SimpleAvData.append(self.candles.close(x))
					SimpleAvData.pop(0)

					ExpAvData.append(self.candles.close(x))
					ExpAvData.pop(0)

					SimpleAv20,SimpleAv50 = self.MMS(SimpleAvData)
					ExpAvData30, prevExpAv30 = self.MME(ExpAvData30, self.candles.close(x), 30)
					ExpAvData20, prevExpAv20 = self.MME(ExpAvData20, self.candles.close(x), 20)

					# print("SimpleAvg = ", SimpleAv20)
					# print("ExpAvg30 = ", ExpAvData30)
					# print("ExpAvg20 = ", ExpAvData20)
					
					if firstIteration:
						if SimpleAv20 > ExpAvData20 and SimpleAv20 > ExpAvData30:
							onTop = 'SimpleMM'
						else:
							onTop = 'ExponentialMM'
						firstIteration = False

					if self.candles.close(x-1) > PrevSimpleAv20 and self.candles.close(x) < SimpleAv20:
						#print ('comprar')
						pass

					if self.candles.close(x-1) > PrevSimpleAv20 and self.candles.close(x) < SimpleAv20:
						#print ('vender')
						pass

					onTop = self.checkCross(SimpleAv20, ExpAvData20, ExpAvData30, onTop)
					#implementar medias curtas cruzando longas ou exponenciais



					'''
					#Lembrar de colocar para nao comprar novamente nos candles futuros ate ocorrer um ponto de venda
					if SimpleAv > ExpAvData30 and SimpleAv > ExpAvData20 :
						comprou -= self.candles.open(x)

					if SimpleAv < ExpAvData30 and SimpleAv < ExpAvData20 :
						comprou += self.candles.open(x)
					'''

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

	def checkCross(self, SimpleMM, Expo20MM, Expo30MM, onTop):
		if onTop == "SimpleMM":
			if Expo20MM > SimpleMM and Expo30MM > SimpleMM:
				onTop = "ExponentialMM"
				print("Simple = ", SimpleMM)
				print("Exp20 = ", Expo20MM)
				print("Exp30 = ", Expo30MM)
				print("Compre tudo VIAAAAADO")
				print("\n\n\n")
		elif onTop == "ExponentialMM":
			if SimpleMM > Expo20MM and SimpleMM > Expo30MM:
				onTop = "SimpleMM"
				print("Simple = ", SimpleMM)
				print("Exp20 = ", Expo20MM)
				print("Exp30 = ", Expo30MM)
				print("Vende tudo VIAAADO")
				print("\n\n\n")
		return onTop	


if __name__ == "__main__":
	startTime = '20170901'
	endTime = '20171001'
	period	= '15'

	trader = Trader('','',startTime,endTime,period)
	trader.Connection()
	#trader.Get_Ticker()
	trader.getCandleHistoricalData()
	trader.BacktestEstrategy()
	
