import socket
import struct
import threading
import json

def server():
	UDP_IP = "127.0.0.1"
	UDP_PORT = 5006
	global sock
	global response
	sock.settimeout(45)
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		response = json.loads(data.decode())
		#join game response, 1=success
		print(response.get("message"))
		print("==============================\n\n")
		if (response.get("id")==0):
			if (response.get("status")=="success"):
				if (response.get("playerAmount")==1):
					print("Server waiting for another player...")
				else:
					print("2 Players ingame, starting game...")
				response={"id" : 0, "status" : "success"}
				s = json.dumps(response).encode()
				sock.sendto(s, ( addr[0], addr[1] ))
				print ("Liityit peliin")
			else:
				print ("Full game or no work")
				joinGame()
		elif (response.get("id")==1): #hit response from server
			#
			print("hitted")
		elif (response.get("id")==2): #stand response from server
			#
			print(response.get("message")) # quit response
		elif (response.get("id")==3):
			#
			print("quit")
		elif (response.get("id")==4): #error response, server waiting for someone else
			print(response.get("message"))
		elif (response.get("id")==5): #state response, gives info for state
			if (response.get("state")=="dealing"):
				print("Game started, dealer dealing")

		
UDP_IP = "127.0.0.1"
UDP_PORT_SERVER = 5005
MESSAGE = "Hello, World!"
UDP_PORT = 5006
#UDP_PORT=int(input("ana portti"))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
try:
	sock.bind((UDP_IP, UDP_PORT))
except OSError:
	sock.bind((UDP_IP, UDP_PORT+1))

t = threading.Thread(target=server)
t.start()
print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT_SERVER)
print ("message:", MESSAGE)

def joinGame(server_ip=UDP_IP):
	#server_ip=input("Anna palvelimen IP osoite: ")
	print ("Joining game...")
	print ("--------------------------\n\n")
	try:
		request={"id" : 0}
		data=json.dumps(request)
		sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
		#print(sock)
	except:
		joinGame()
		
def sendHitRequest(server_ip):
	try:
		request={"id" : 1}
		data=json.dumps(request)
		sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
	except:
		sendHitRequest(server_ip)
		
def sendStandRequest(server_ip):
	try:
		request={"id" : 2}
		data=json.dumps(request)
		sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
	except:
		sendHitRequest(server_ip)
		
def sendExitMessage(server_ip):
	try:
		request={"id" : 3}
		data=json.dumps(request)
		sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
	except:
		sendHitRequest(server_ip)

server_ip='127.0.0.1'
response=""
commands = {0 : joinGame,
           1 : sendHitRequest,
           2 : sendStandRequest,
           3 : sendExitMessage,
}
while True:
	try:
		command=int(input("give command: "))
		try:
			commands[command](server_ip)
		except KeyError:
			print("Give a proper command")
		print("\n\n")
	except ValueError:
		continue

	command=None
#message = ""
#message += struct.pack("i",4)
#message += struct.pack("i",3)
#sock.sendto(message, (UDP_IP, UDP_PORT_SERVER))