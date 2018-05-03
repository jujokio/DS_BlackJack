"""
Edited from https://gist.github.com/mjhea0/5680216
"""
import os
import random

deck = []
class Player():
	hand=[]
	name = None
	def __init__(self, name=None):
		self.name = name
		
	def setHand(self, hand):
		self.hand = hand
	def getHand(self):
		return self.hand
	def setName(self, name):
		self.name = name
	def getName(self):
		return self.name
		
		
		
class BlackJackGameObject():
	player1 = Player()
	player2 = Player()
	dealer = Player()
	deck = []


	def __init__(self):
		deck = self.createDeck()
		game = self.game()
		
		
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
		for j in range(4):
			for i in range(1,15):
				deck.append(i)
		print(deck)
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
		exit()

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
		card = deck.pop()
		if card == 11:card = "J"
		if card == 12:card = "Q"
		if card == 13:card = "K"
		if card == 14:card = "A"
		hand.append(card)
		return hand

	def clear(self):
		if os.name == 'nt':
			os.system('CLS')
		if os.name == 'posix':
			os.system('clear')

	def print_results(self, dealer_hand, player_hand):
		self.clear()
		print ("The dealer has a " + str(dealer_hand) + " for a total of " + str(self.total(dealer_hand)))
		print ("You have a " + str(player_hand) + " for a total of " + str(self.total(player_hand)))

	def blackjack(self, dealer_hand, player_hand):
		if self.total(player_hand) == 21:
			self.print_results(dealer_hand, player_hand)
			print ("Congratulations! You got a Blackjack!\n")
			self.play_again()
		elif self.total(dealer_hand) == 21:
			self.print_results(dealer_hand, player_hand)		
			print ("Sorry, you lose. The dealer got a blackjack.\n")
			self.play_again()

	def score(self, dealer_hand, player_hand):
		if self.total(player_hand) == 21:
			self.print_results(dealer_hand, player_hand)
			print ("Congratulations! You got a Blackjack!\n")
		elif self.total(dealer_hand) == 21:
			self.print_results(dealer_hand, player_hand)		
			print ("Sorry, you lose. The dealer got a blackjack.\n")
		elif self.total(player_hand) > 21:
			self.print_results(dealer_hand, player_hand)
			print ("Sorry. You busted. You lose.\n")
		elif self.total(dealer_hand) > 21:
			self.print_results(dealer_hand, player_hand)			   
			print ("Dealer busts. You win!\n")
		elif self.total(player_hand) < self.total(dealer_hand):
			self.print_results(dealer_hand, player_hand)
			print ("Sorry. Your score isn't higher than the dealer. You lose.\n")
		elif self.total(player_hand) > self.total(dealer_hand):
			self.print_results(dealer_hand, player_hand)			   
			print ("Congratulations. Your score is higher than the dealer. You win\n")		
		
		
	def scoreOneHand(self, hand):
		if self.total(hand) == 21:
			print ("Congratulations! You got a Blackjack!\n")
			self.play_again()
		elif self.total(hand) > 21:
			print ("Sorry. You busted with %s. You lose.\n" %str(hand))
			self.play_again()	
		
	def game(self):
		choice = 0
		self.clear()
		print ("WELCOME TO DISTRIBUTED BLACKJACK!\n")
		
		self.player1.setHand(self.deal(deck))
		self.player2.setHand(self.deal(deck))
		self.dealer.setHand(self.deal(deck))
		
		while choice != "q":
			print ("The dealer is showing a " + str(self.dealer.getHand()[0]))
			print ("You have a " + str(self.player1.getHand()) + " for a total of " + str(self.total(self.player1.getHand())))
			self.blackjack(self.dealer.getHand(), self.player1.getHand())
			choice = input("Do you want to [H]it, [S]tand, or [Q]uit: ")
			choice = choice.lower()
			self.clear()
			if choice == "h":
				self.hit(self.player1.getHand())
				self.scoreOneHand(self.player1.getHand())
			elif choice == "s":
				while self.total(self.dealer.getHand()) < 17:
					self.hit(self.dealer.getHand())
				self.score(self.dealer.getHand(), self.player1.getHand())
				self.play_again()
			elif choice == "q":
				print ("Bye!")
				exit()
		
