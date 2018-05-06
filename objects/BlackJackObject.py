"""
Edited from https://gist.github.com/mjhea0/5680216
"""
import os
import random
from server import *
import socket
import struct
import sys
import threading
import json
import time
deck = []

class Player():
	hand=[]
	name = None
	port = ""
	ip = ""
	isPlaying = True
	def __init__(self, ip, port,  name=None):
		self.name = name
		self.port = port
		self.ip = ip		
	def setHand(self, hand):
		self.hand = hand
	def getHand(self):
		return self.hand
	def setName(self, name):
		self.name = name
	def getName(self):
		return self.name
	def getIP(self):
		return self.ip
	def getPort(self):
		return self.port	
	def setPlaying(self):
		self.isPlaying = not self.isPlaying
	
	
		
		
class BlackJackGameObject():
	playerList = []
	dealer = Player(0,0)
	deck = []
	game = None
	sock = None
	gameTime=2
	

	def __init__(self):
		self.deck = self.createDeck()
		#game = self.game()
		t = threading.Thread(target=timer)
		t.start()
				
	def bindSocket(self):
		UDP_IP = "127.0.0.1"
		UDP_PORT = 5005
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		self.sock.bind((UDP_IP, UDP_PORT))
		self.sock.settimeout(45)

	def waitForPlayers(self):
		time =0
		while len(self.playerList) <= 1:
			
			print("Waiting for players:")
			client_ip, client_port = server(self.sock)
			#self.player1 = Player(client_ip, client_port)
			player = Player(client_ip, client_port)
			self.playerList.append(player)

			#print(client_ip, client_port)
			playersAmount=len(self.playerList)
			response={"id" : 0, "message" : "WELCOME TO DISTRIBUTED BLACKJACK!\n", "status" : "success", "playerAmount" : playersAmount}
			s = json.dumps(response).encode()
			sendMessageAndReceiveResponse(self.sock, player.getIP(), player.getPort(), s)
		
	def running(self):
		return True if game is not None else None	
		
	def getHands(self):
		hands = {
			"player1":player1.getHand(),
			"player2":player2.getHand(),
			"dealer":dealer.getHand(),
		}
		return hands
	
	def createDeck(self):
		deck = []
		for j in range(4):
			for i in range(2,15):
				deck.append(i)
		return deck

	def deal(self, deck):
		hand = []
		for i in range(2):
			random.shuffle(deck)
			card = deck.pop()
			if card == 11:card = "J"
			if card == 12:card = "Q"
			if card == 13:card = "K"
			if card == 14:card = "A"
			hand.append(card)
		return hand

	def play_again(self):
		print("end here")

		self.game=None
		self.__init__()
		#exit()

	def total(self, hand):
		total = 0
		for card in hand:
			if card == "J" or card == "Q" or card == "K":
				total+= 10
			elif card == "A":
				if total >= 11: 
				   total+= 1
				else: 
				   total+= 11
			else:
				total += card
		return total

	def hit(self, hand):
		card = self.deck.pop()
		if card == 11:card = "J"
		if card == 12:card = "Q"
		if card == 13:card = "K"
		if card == 14:card = "A"
		hand.append(card)
		return hand

	def clear(self):
		return
		if os.name == 'nt':
			os.system('CLS')
		if os.name == 'posix':
			os.system('clear')

	def print_results(self, dealer_hand, player_hand):
		self.clear()
		return ("The dealer has a " + str(dealer_hand) + " for a total of " + str(self.total(dealer_hand)))
		return ("You have a " + str(player_hand) + " for a total of " + str(self.total(player_hand)))
		
	def blackjack(self, dealer_hand, player_hand):
		if self.total(player_hand) == 21:
			self.print_results(dealer_hand, player_hand)
			print ("Congratulations! You got a Blackjack!\n")
			return True
			#self.play_again()
		elif self.total(dealer_hand) == 21:
			self.print_results(dealer_hand, player_hand)		
			print ("Sorry, you lose. The dealer got a blackjack.\n")
			return True
			#self.play_again()
		else:
			return False

	def score(self, dealer_hand, player_hand):
		if self.total(player_hand) == 21:
			return self.print_results(dealer_hand, player_hand)
			print ("Congratulations! You got a Blackjack!\n")
		elif self.total(dealer_hand) == 21:
			return self.print_results(dealer_hand, player_hand)		
			print ("Sorry, you lose. The dealer got a blackjack.\n")
		elif self.total(player_hand) > 21:
			return self.print_results(dealer_hand, player_hand)
			print ("Sorry. You busted. You lose.\n")
		elif self.total(dealer_hand) > 21:
			return self.print_results(dealer_hand, player_hand)			   
			print ("Dealer busts. You win!\n")
		elif self.total(player_hand) < self.total(dealer_hand):
			return self.print_results(dealer_hand, player_hand)
			print ("Sorry. Your score isn't higher than the dealer. You lose.\n")
		elif self.total(player_hand) > self.total(dealer_hand):
			return self.print_results(dealer_hand, player_hand)			   
			print ("Congratulations. Your score is higher than the dealer. You win\n")		
		
	def scoreOneHand(self, hand):
		if self.total(hand) == 21:
			print ("Congratulations! You got a Blackjack!\n")
			#self.play_again()
			return True
		elif self.total(hand) > 21:
			print ("Sorry. You busted with %s. You lose.\n" %str(hand))
			#self.play_again()
			return True	

	def game(self):
		print(self.gameTime)
		choice = 0
		self.clear()
		self.dealer.setHand(self.deal(self.deck))
		#deal hands
		for player in self.playerList:
				player.setHand(self.deal(self.deck))

		#player plays
		for player in self.playerList:
			#lähetä your turn
			message = "The dealer is showing a " + str(self.dealer.getHand()[0]) + " \n\nYou have a " + str(player.getHand()) + " for a total of " + str(self.total(player.getHand()))
				
			response={"id" : 6, "message" : message, "status" : "success", "state" : "yourturn"}
			s = json.dumps(response).encode()
			#send status
			sendMessageAndReceiveResponse(self.sock, player.getIP(), player.getPort(), s)

			while player.isPlaying:
				print ("The dealer is showing a " + str(self.dealer.getHand()[0]))
				print ("\n\nYou have a " + str(player.getHand()) + " for a total of " + str(self.total(player.getHand())))

				if not self.blackjack(self.dealer.getHand(), player.getHand()):

					#create status message
					message = "The dealer is showing a " + str(self.dealer.getHand()[0]) + " \n\nYou have a " + str(player.getHand()) + " for a total of " + str(self.total(player.getHand()))
					
					response={"id" : 5, "message" : message}
					s = json.dumps(response).encode()
					#send status
					responseJson = sendMessageAndReceiveResponse(self.sock, player.getIP(), player.getPort(), s)

					choice = responseJson.get("id")
					choice = int(choice)
					self.clear()
					if choice == 1:
						self.hit(player.getHand())
						if self.scoreOneHand(player.getHand()):
							player.setPlaying()
					elif choice == 2:
						player.setPlaying()
						#self.play_again()
					elif choice == 3:
						print ("Bye!")
						player.setPlaying()
						#exit()
						#self.game=None
						#self.__init__()
				else:
					#player or delare black jack!
					player.setPlaying()
					print("BLACK JACK idk?")


			# player ends their turn
			message = "The dealer is showing a " + str(self.dealer.getHand()[0]) + " \n\nYou have a " + str(player.getHand()) + " for a total of " + str(self.total(player.getHand()))
				
			response={"id" : 6, "message" : message, "status" : "success", "state" : "endOfTurn"}
			s = json.dumps(response).encode()
			#send status
			sendMessageAndReceiveResponse(self.sock, player.getIP(), player.getPort(), s)

		# dealer plays his hand
		while self.total(self.dealer.getHand()) < 17:
			self.hit(self.dealer.getHand())

		for player in self.playerList:
			message = self.score(self.dealer.getHand(),player.getHand())

			#message = "The dealer is showing a " + str(self.dealer.getHand()[0]) + " \n\nYou have a " + str(player.getHand()) + " for a total of " + str(self.total(player.getHand()))
				
			response={"id" : 6, "message" : message, "status" : "success", "state" : "endOfGame"}
			s = json.dumps(response).encode()
			#send status
			responseJson = sendMessageAndReceiveResponse(self.sock, player.getIP(), player.getPort(), s)
			player.setPlaying()

		self.deck = self.createDeck()
		#self.sock.close()
		