import socket
import sys

from objects import ServerObject
from objects import ClientObject



if __name__ == "__main__":
	
	ready_to_receive = False
	
	try:
		print("hello World")
		server = ServerObject.ServerObject()
		client = ClientObject.ClientObject()
		ready_to_receive = server.ReceiveJoinRequest()
		game = server.startGame()
		game.start()
		while ready_to_receive and game.running():
			if client.SendJoinRequest():
				ready_to_receive = False
			print("playing the game lol...")
		
	except KeyboardInterrupt:
		sys.exit(1)
	