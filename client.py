import socket
import struct
import threading
import json

def server():
	UDP_IP = "127.0.0.1"
	UDP_PORT = 5006
	global sock
	global response
	sock.settimeout(10)
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		print("jou")
		response = json.loads(data.decode())
		#join game response, 1=success
		print(response)
		if (response.get("id")==0):
			if (response.get("message")=="success"):
				print ("Liityit peliin")
			else:
				print ("Full game or no work")
				joinGame()
		if (response.get("id")==1):
			#
			print("toinen request")
		print ("received message:", response)

		
UDP_IP = "127.0.0.1"
UDP_PORT_SERVER = 5005
MESSAGE = "Hello, World!"
UDP_PORT = 5006
#UDP_PORT=int(input("ana portti"))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
t = threading.Thread(target=server)
t.start()
print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT_SERVER)
print ("message:", MESSAGE)

def joinGame():
	server_ip=input("Anna palvelimen IP osoite: ")
	server_ip='127.0.0.1'
	print ("Joining game")
	print ("--------------------------")
	try:
		request={"id" : 0}
		data=json.dumps(request)
		sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
		print(sock)
	except:
		joinGame()
		
response=""
joinGame()
#message = ""
#message += struct.pack("i",4)
#message += struct.pack("i",3)
#sock.sendto(message, (UDP_IP, UDP_PORT_SERVER))