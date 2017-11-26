class Candle:
	candle_list = []
	
	def __init__(self, historical_candles):
		self.candle_list = historical_candles
		
	def __len__(self):
		return len(self.candle_list)

	def printCandle(self, index):
		return self.candle_list[index]

	def high(self, index):
		return self.candle_list[index]['high']

	def low(self, index):
		return self.candle_list[index]['low']

	def volume(self, index):
		return self.candle_list[index]['volume']

	def open(self, index):
		return self.candle_list[index]['open']

	def close(self, index):
		return self.candle_list[index]['close']