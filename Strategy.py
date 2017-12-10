class BacktestStrategy:

	def SimpleAVPrice(self,player,candle,SimpleAv20,PrevSimpleAv20):


		if candle[0] > PrevSimpleAv20 and candle[0] < SimpleAv20:
			player.Venda(candle[0],candle[1])
			
	
		if candle[0] < PrevSimpleAv20 and candle[0] > SimpleAv20:
			player.Compra(candle[0],candle[1])
			


	def ExpSimpleAv(self,player,candle,SimpleAv,Avg20,Avg30):
		if SimpleAv > Avg30 and SimpleAv > Avg20 :
			player.Compra(candle[0],candle[1])


		if SimpleAv < Avg30 and SimpleAv < Avg20 :
			player.Venda(candle[0],candle[1])



	
