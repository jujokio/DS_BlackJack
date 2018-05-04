import socket
import sys

from objects import BlackJackObject



if __name__ == "__main__":
	
	while True:
		try:
			game = BlackJackObject.BlackJackGameObject()
			game.bindSocket()
			game.waitForPlayers()
			game.game()
		except KeyboardInterrupt:
			sys.exit(1)
