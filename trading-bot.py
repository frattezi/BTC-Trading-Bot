import time
import sys, getopt
import datetime
from poloniex import poloniex

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
		candles = historicalData
	
	print(candles)

	prices = prices[-lengthOfMA:]
	if (not startTime):
		time.sleep(int(period))


if __name__ == "__main__":
	main(sys.argv[1:])