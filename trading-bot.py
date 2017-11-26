import time
import sys, getopt
import datetime
from poloniex import poloniex

class Candle:
	candle_list = []
	
	def __init__(self, historical_candles):
		self.candle_list = historical_candles

	def printCandle(self, index):
		return self.candle_list[index]

	def high(self, index):
		return self.candle_list[index]['high']

	def low(self, index):
		return self.candle_list[index]['low']

	def volume(self, index):
		return self.candle_list[index]['volume']

	def open(self, index);
		return self.candle_list[index]['open']

	def close(self, index):
		return self.candle_list[index]['close']


def main(argv):
	period = 900
	pair = "USDT_BTC"
	prices = []
	currentMovingAverage = 0;
	lengthOfMA = 0
	startTime = "1508797168"
	endTime = "1511475568"
	historicalData = False
	candles = False
	tradePlaced = False
	typeOfTrade = False
	dataDate = ""
	orderNumber = ""

	try:
		opts, args = getopt.getopt(argv,"hp:c:n:s:e:",["period=","currency=","points="])
	except getopt.GetoptError:
		print 'trading-bot.py -p <period length> -c <currency pair> -n <period of moving average>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'trading-bot.py -p <period length> -c <currency pair> -n <period of moving average>'
			sys.exit()
		elif opt in ("-p", "--period"):
			if (int(arg) in [300,900,1800,7200,14400,86400]):
				period = arg
			else:
				print 'Poloniex requires periods in 300,900,1800,7200,14400, or 86400 second increments'
				sys.exit(2)
		elif opt in ("-c", "--currency"):
			pair = arg
		elif opt in ("-n", "--points"):
			lengthOfMA = int(arg)
		elif opt in ("-s"):
			startTime = arg
		elif opt in ("-e"):
			endTime = arg



	conn = poloniex('key goes here','key goes here')

	if (startTime):
		historicalData = conn.api_query("returnChartData",{"currencyPair":pair,"start":startTime,"end":endTime,"period":period})

		candles = Candle(historicalData)
	
	#print("Candles = ", candles[0]['low'])
	print("volume = ", candles.getVolume(0))
	print("Candle = ", candles.printCandle(0))

	prices = prices[-lengthOfMA:]
	if (not startTime):
		time.sleep(int(period))


if __name__ == "__main__":
	main(sys.argv[1:])