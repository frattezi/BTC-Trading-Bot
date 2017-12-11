import pandas as pd
class Player:
	
	def __init__(self):
		self.initial_invest = 30000
		self.money = 30000
		self.quantidade_ativos = 0
		self.compras_realizadas = []
		self.vendas_realizadas = []
		self.compras_vector = []
		self.vendas_vector = []
		self.stop_limit = 2000
		self.lucro = 0

	
	def PlayerRules(self,valor):
		if self.money < valor:
			return False
		else:
			return True


	def Venda(self, valor,date):
		if self.quantidade_ativos > 0:
			self.money = self.money + valor
			self.quantidade_ativos = self.quantidade_ativos - 1
			self.vendas_vector.append([valor,date])
	
	def Compra(self, valor,date):
		if self.PlayerRules(valor):
			print ('Compra')
			self.money = self.money - valor
			self.quantidade_ativos = self.quantidade_ativos + 1
			self.compras_vector.append([valor,date])
		else:
			print ('Compra negada por falta de dinheiro em caixa')

	def getMoney(self):
		return self.money

	def getLucro(self,btc_current_value):
		self.lucro = self.money + self.CheckBtcBalance(btc_current_value) - self.initial_invest
		return self.lucro

	def CheckBtcBalance(self,btc_current_value):
		BTCBalance = self.quantidade_ativos*btc_current_value
		return BTCBalance


	def SowFinalResults(self,btc_current_value):
		print ('Investimento inicial: ',self.initial_invest)
		print ('Total de compras realizadas: ',len(self.compras_vector))
		print ('Total de vendas realizadas: ',len(self.vendas_vector))
		print ('Valor atual na carteira: ',self.money)
		print ('Valor em btc: ', self.CheckBtcBalance(btc_current_value))
		print ('Lucro ou prejuizo Final: ',self.getLucro(btc_current_value))
		df = pd.DataFrame(self.compras_vector)
		print ('compras:')
		print (df)
		print ('vendas:')
		df = pd.DataFrame(self.vendas_vector)
		print(df)