class Player:
	
	def __init__(self):
		self.money = 15000
		self.quantidade_ativos = 0
		self.compras_realizadas = 0
		self.vendas_realizadas = 0
		self.lucro = 0

	def Venda(self, valor):
		self.money = self.money + valor
		self.quantidade_ativos = self.quantidade_ativos - 1
		self.vendas_realizadas = self.vendas_realizadas + 1
	
	def Compra(self, valor):
		self.money = self.money - valor
		self.quantidade_ativos = self.quantidade_ativos + 1
		self.compras_realizadas = self.compras_realizadas + 1

	def getMoney(self):
		return self.money

	def getLucro(self):
		self.lucro = self.money - 15000
		return self.lucro