class BacktestStrategy:

	def SimpleAVPrice(self,player,candle,SimpleAv20,PrevSimpleAv20):


		if candle[0] > PrevSimpleAv20 and candle[0] < SimpleAv20:
			print ('Venda')
			player.Venda(candle[0],candle[1])
			
	
		if candle[0] < PrevSimpleAv20 and candle[0] > SimpleAv20:
			print ('compra')
			player.Compra(candle[0],candle[1])
			


	def ExpSimpleAv(self, SimpleMM, Expo20MM, Expo30MM, onTop, player, candle):
		if onTop == "SimpleMM":
			if Expo20MM > SimpleMM and Expo30MM > SimpleMM:
				onTop = "ExponentialMM"
				print("Simple = ", SimpleMM)
				print("Exp20 = ", Expo20MM)
				print("Exp30 = ", Expo30MM)
				print("Compre tudo VIAAAAADO")
				print("\n\n\n")
				player.Compra(candle[0], candle[1])
		elif onTop == "ExponentialMM":
			if SimpleMM > Expo20MM and SimpleMM > Expo30MM:
				onTop = "SimpleMM"
				print("Simple = ", SimpleMM)
				print("Exp20 = ", Expo20MM)
				print("Exp30 = ", Expo30MM)
				print("Vende tudo VIAAADO")
				print("\n\n\n")
				player.Venda(candle[0], candle[1])
		return onTop


	# def ExpSimpleAv(self):
	# 	if SimpleAv > Avg30 and SimpleAv > Avg20 :
	# 			compra




	# 		if SimpleAv < Avg30 and SimpleAv < Avg20 :

	# 				venda



	
