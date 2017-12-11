import pandas as pd

class Candle:
	candle_list = []
	
	def __init__(self, historical_candles):
		df = pd.DataFrame(historical_candles)
		df['date'] = pd.to_datetime(df["date"], unit='s')
		self.candle_list = df
		print (self.candle_list)
		
	def __len__(self):
		return len(self.candle_list)

	def printCandle(self, index):
		return self.candle_list.ix[index]

	def high(self, index):
		return self.candle_list['high'][index]

	def low(self, index):
		return self.candle_list['low'][index]

	def volume(self, index):
		return self.candle_list['volume'][index]

	def open(self, index):
		return self.candle_list['open'][index]

	def close(self, index):
		return self.candle_list['close'][index]

	def date(self,index):
		return self.candle_list['date'][index]

	def CloseDate(self,index):
		return [self.candle_list['close'][index],self.candle_list['date'][index]]

	def getClose(self):
		return self.candle_list['close']

	def high2(self):
		return self.candle_list['high']

	def low2(self):
		return self.candle_list['low']

	def open2(self):
		return self.candle_list['open']

	def close2(self):
		return self.candle_list['close']

	def getTime(self, x):
		return self.candle_list['date'][x]
	