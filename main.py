import pandas as pd
import numpy as np
import queuezed

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

	def atualizar_candles(self, Queue1, Queue2, Queue3, candle_value):
		Queue1.dequeue()#deletar ultima item da fila
		Queue2.dequeue()
		Queue3.dequeue()
		Queue1.enqueue(candle_value)#inserir na fila
		Queue2.enqueue(candle_value)
		Queue3.enqueue(candle_value)
		return Queue1, Queue2, Queue3

	def Estrategy(self):
		SimpleAvData = queuezed.Queue()#Queuezuda
		ExpAvData20 = queuezed.Queue()
		ExpAvData30 = queuezed.Queue()
		Avg30 = []
		Avg20 = []
		prevExpAv30 = None
		prevExpAv20	= None
		Avg30 = 0
		Avg20 = 0
		SimpleAv = 0
		comprou = 0
		actual_currency = 0
		quantidade_comprada = 0
		for x in range(0,len(self.candles)):
			#starting average vectors
			if x <	50:#take first 50 candles
				SimpleAvData.enqueue(self.candles.close(x))
				if x >= 20 and x < 50:#take 30 first candles
					ExpAvData30.enqueue(self.candles.close(x))
				if x >= 30 and x < 50:#take 20 first candles
					ExpAvData20.enqueue(self.candles.close(x))
			else:
				self.atualizar_candles(SimpleAvData, ExpAvData20, ExpAvData30, self.candles.close(x))
				SimpleAv = self.MMS(SimpleAvData)
				Avg30, prevExpAv30 = self.MME(ExpAvData30,prevExpAv30,30)
				Avg20, prevExpAv20 = self.MME(ExpAvData20,prevExpAv20,20)
				# print("SIMPLE AV = ", SimpleAv)
				# print("ExpAV20 = ", Avg20)
				# print("ExpAV30 = ", Avg30)
				
				#Lembrar de colocar para nao comprar novamente nos candles futuros ate ocorrer um ponto de venda
				if SimpleAv > Avg30 and SimpleAv > Avg20 :
#					print ('')
					comprou -= self.candles.open(x)
					actual_currency = self.candles.open(x)
					quantidade_comprada = quantidade_comprada + 1
					#print("Compre1")

				if SimpleAv < Avg30 and SimpleAv < Avg20 :
					if quantidade_comprada > 0:
						comprou += self.candles.open(x)
						actual_currency = self.candles.open(x)
						quantidade_comprada = quantidade_comprada - 1
						#print("Vendi1")
		
		for i in range(0, quantidade_comprada):
			comprou = comprou + actual_currency
		print (comprou)
		print ('e isso ai')


	#Media Movel Simples
	def MMS(self,SimpleAvData):
		return np.average(SimpleAvData.getList())

	#Media Movel Exponencial
	def MME(self,ExpAvData,prevEMA,period):
		multiplier = None
		print("OIOI", ExpAvData)
		if prevEMA == None:
			mms = self.MMS(ExpAvData)
			multiplier = (2/(period+1))
			mme = (ExpAvData[len(ExpAvData)-1] - mms)*multiplier+mms
			print("MME = ", mme)
			print("MMS = ", mms)
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
	
