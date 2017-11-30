class BacktestStrategy:

	def SimpleAVPrice(self,player,candle,SimpleAv20,PrevSimpleAv20):


		if candle[0] > PrevSimpleAv20 and candle[0] < SimpleAv20:
			print ('Venda')
			player.Venda(candle[0],candle[1])
			
	
		if candle[0] < PrevSimpleAv20 and candle[0] > SimpleAv20:
			print ('compra')
			player.Compra(candle[0],candle[1])
			