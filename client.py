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
UDP_PORT_SERVER = 10001
UDP_PORT = 5006

def flush_input():
    try: 
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def server():
	global sock
	global response
	global ingame
	global yourTurn
	sock.settimeout(60)
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		response = json.loads(data.decode())
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
			
		elif (response.get("id")==5): #error response, server waiting for someone else
			clear("")
			print("============SERVER============\n\n")
			print(response.get("message"))
			print("==============================\n\n")
			print("Commands:\n 0 = Joingame\n 1 = Hit\n 2 = Stand\n 3 = Quit\n 4 = Clear console\n")
			print("Give command:")
			
		elif (response.get("id")==6): #state response, gives info for state
			if (response.get("state")=="dealing"):
				print("Game started, dealer dealing")
			elif (response.get("state")=="yourturn"):
				yourTurn=True
				ingame = True
			elif (response.get("state")=="endOfTurn"):
				yourTurn=False
				clear("")
				print("============SERVER============\n\n")
				print(response.get("message"))
				print("==============================\n\n")
				print("Your turn ended.")
			elif (response.get("state")=="endOfGame"):
				yourTurn=False
				ingame = True
				clear("")
				print("Game ended.")
				print("*"*10)
				print(response.get("message"))
				print("*"*10)
				print("Waiting for new game...")
			response={"id" : 6, "status" : "success"}
			s = json.dumps(response).encode()
			sock.sendto(s, ( addr[0], addr[1] ))
		response = None
		


def joingame(server_ip):
	global ingame
	global yourTurn
	if not ingame and not yourTurn:
		print ("Joining game...")
		try:
			request={"id" : 0}
			data=json.dumps(request)
			sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
		except:
			print("Something went wrong.")
		
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
			
server_ip=input("Give blackjack server ip: ")
if (server_ip=="0"):
	server_ip="130.231.60.50"
response=""

commands = {0 : joingame,
           1 : sendHitRequest,
           2 : sendStandRequest,
           3 : sendExitMessage,
		   4 : clear,
}

global sock
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
for i in range(0, 30):
	try:
		print(UDP_PORT+i)
		sock.bind(("0.0.0.0", UDP_PORT+i))
		break
	except OSError:
		continue

t = threading.Thread(target=server)
t.start()
print ("UDP target IP:", server_ip)
print ("UDP target port:", UDP_PORT_SERVER)
print("Commands:\n 0 = Joingame\n 1 = Hit\n 2 = Stand\n 3 = Quit\n 4 = Clear console\n")

while True:
	if (yourTurn or not ingame):
		try:
			flush_input()
			command=int(input())
			try:
				commands[command](server_ip)
				command=None
			except KeyError:
				print("Give a proper command")
				command=None
			print("\n\n")
		except ValueError:
			command=None