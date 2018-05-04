import socket
from . import BlackJackObject
	
		
class ServerObject():
	game = None

	
	def __init__(self):
		print("server init")
		servu = self.start()

	def ReceiveJoinRequest(self):
		print("server Joining...")
		requestCode = 0
		return True
		
		
	def ReceiveStandRequest(self):
		print("server Standing...")
		requestCode = 1
		return None

	def ReceiveHitRequest(self):
		print("server Hitting...")
		requestCode = 2
		return None	
		
		
	def ReceiveRageQuitRequest(self):
		print("server Quiting...")
		requestCode = -1
		return None
		
		
		
	def ReceiveRequest(self):
		print("server requesting...")
		return None
		
	def startGame(self):
		self.game = BlackJackObject.BlackJackGameObject()
		self.game.game()
		print("serverObject uusipeli")
		
		
		
	def start(self):
		print("server start")
		return self.game
	
	
		