class BacktestStrategy:

	def SimpleAVPrice(self,player,candle,SimpleAv20,PrevSimpleAv20):


		if candle[0] > PrevSimpleAv20 and candle[0] < SimpleAv20:
			player.Venda(candle[0],candle[1])
			
	
		if candle[0] < PrevSimpleAv20 and candle[0] > SimpleAv20:
			player.Compra(candle[0],candle[1])
			


	def ExpSimpleAv(self, SimpleMM, Expo20MM, Expo30MM, onTop, player, candle):
		if onTop == "SimpleMM":
			if Expo20MM > SimpleMM and Expo30MM > SimpleMM:
				onTop = "ExponentialMM"
				player.Compra(candle[0], candle[1])


		elif onTop == "ExponentialMM":
			if SimpleMM > Expo20MM and SimpleMM > Expo30MM:
				onTop = "SimpleMM"
				player.Venda(candle[0], candle[1])
		return onTop
