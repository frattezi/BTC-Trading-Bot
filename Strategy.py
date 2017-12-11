class BacktestStrategy:

	def SimpleAVPrice(self,player,candle,SimpleAv20,PrevSimpleAv20):


		if candle[0] > PrevSimpleAv20 and candle[0] < SimpleAv20:
			player.Venda(candle[0],candle[1])
			
	
		if candle[0] < PrevSimpleAv20 and candle[0] > SimpleAv20:
			player.Compra(candle[0],candle[1])
			


	def ExpSimpleAv(self, SimpleMM, Expo20MM, Expo30MM, onTop):
		if onTop == "SimpleMM":
			if Expo20MM > SimpleMM and Expo30MM > SimpleMM:
				onTop = "ExponentialMM"
				return onTop,'BUY'

		elif onTop == "ExponentialMM":
			if SimpleMM > Expo20MM and SimpleMM > Expo30MM:
				onTop = "SimpleMM"
				return onTop, 'SELL'
		return onTop,'IDLE'

