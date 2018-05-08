import socket
import sys
import time
import threading

from objects import BlackJackObject


if __name__ == "__main__":
	print("Starting the DBJ server...")
	game = BlackJackObject.BlackJackGameObject()
	game.bindSocket()
	
	while True:
		try:
			game.waitForPlayers()
			game.game()
		except KeyboardInterrupt:
			sys.exit(1)
