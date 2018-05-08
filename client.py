import socket
import struct
import threading
import json
import os
import sys


#variables
global ingame
global yourTurn
ingame=False
yourTurn=False

UDP_IP = "127.0.0.1"
UDP_PORT_SERVER = 5005
UDP_PORT = 5006



def server():
	UDP_IP = "127.0.0.1"
	UDP_PORT = 5006
	global sock
	global response
	global ingame
	global yourTurn
	sock.settimeout(45)
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		response = json.loads(data.decode())
		
		print("==============================\n\n")
		print(response.get("message"))
		print("==============================\n\n")
		
		#print("Commands:\n 0 = Joingame\n 1 = Hit\n 2 = Stand\n 3 = Quit\n 4 = Clear console\n")
		if (response.get("id")==0):
			if (response.get("status")=="success"):
				ingame=True
				if (response.get("playerAmount")):
					print(response.get("playerAmount"), "players ingame, starting game in 20sec...")
				response={"id" : 0, "status" : "success"}
				s = json.dumps(response).encode()
				sock.sendto(s, ( addr[0], addr[1] ))
				print ("Liityit peliin")
			else:
				print ("Full game or no work")
				joingame()
							
		elif (response.get("id")==1): #hit response from server
			#
			print("hitted")
		elif (response.get("id")==2): #stand response from server
			#
			print("stand") # quit response
		elif (response.get("id")==3):
			#
			print("quit")
			
		elif (response.get("id")==4): #error response, server waiting for someone else
			print(response.get("message"))
			
		elif (response.get("id")==6): #state response, gives info for state
			if (response.get("state")=="dealing"):
				print("Game started, dealer dealing")
			elif (response.get("state")=="yourturn"):
				yourTurn=True
				ingame = True
			elif (response.get("state")=="endOfTurn"):
				yourTurn=False
				print("Your turn ended.")
			elif (response.get("state")=="endOfGame"):
				yourTurn=False
				ingame = False
				print ("\n\n")
				print("Game ended.")
				print("*"*10)
				print(response.get("message"))
				print("*"*10)
			response={"id" : 6, "status" : "success"}
			s = json.dumps(response).encode()
			sock.sendto(s, ( addr[0], addr[1] ))
		response = None
		


def joingame(server_ip=UDP_IP):
	global ingame
	global yourTurn
	if not ingame and not yourTurn:
		#server_ip=input("Anna palvelimen IP osoite: ")
		print ("Joining game...")
		try:
			request={"id" : 0}
			data=json.dumps(request)
			sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
			#print(sock)
		except:
			joingame()
		
def sendHitRequest(server_ip):
	global ingame
	global yourTurn
	
	if ingame and yourTurn:
		try:
			request={"id" : 1}
			data=json.dumps(request)
			sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
		except:
			sendHitRequest(server_ip)
		
def sendStandRequest(server_ip):
	global ingame
	global yourTurn
	if ingame and yourTurn:
		try:
			request={"id" : 2}
			data=json.dumps(request)
			sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
		except:
			sendHitRequest(server_ip)
		
def sendExitMessage(server_ip):
	global ingame 
	if ingame and yourTurn:
		try:
			request={"id" : 3}
			data=json.dumps(request)
			sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
		except:
			sendHitRequest(server_ip)

			
def clear(ip):
	if os.name == 'nt':
		os.system('CLS')	
	if os.name == 'posix':
		os.system('clear')
			
server_ip='127.0.0.1'
response=""

commands = {0 : joingame,
           1 : sendHitRequest,
           2 : sendStandRequest,
           3 : sendExitMessage,
		   4 : clear,
}


#UDP_PORT=int(input("ana portti"))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
for i in range(0, 30):
	try:
		sock.bind((UDP_IP, UDP_PORT+i))
	except OSError:
		continue

t = threading.Thread(target=server)
t.start()
print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT_SERVER)
print("Commands:\n 0 = Joingame\n 1 = Hit\n 2 = Stand\n 3 = Quit\n 4 = Clear console\n")
while True:
	#print(message)
	if (yourTurn or not ingame):
		try:
			command=int(input("give command: "))
			try:
				commands[command](server_ip)
				command=None
			except KeyError:
				print("Give a proper command")
				command=None
			print("\n\n")
		except ValueError:
			command=None
#message = ""
#message += struct.pack("i",4)
#message += struct.pack("i",3)
#sock.sendto(message, (UDP_IP, UDP_PORT_SERVER))