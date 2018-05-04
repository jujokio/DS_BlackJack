import socket
import struct
import sys
import threading
import json

def server():
	UDP_IP = "127.0.0.1"
	UDP_PORT = 5005

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))
	print(sock)
	players=0
	sock.settimeout(10)
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		request = json.loads(data.decode())
		#Join game
		print (addr)
		if (request.get("id")==0):
			if (players<=2):
				response={"id" : 0, "message" : "success"}
				sock.sendto(json.dumps(response).encode(), (addr[0], addr[1]))
		elif (request.get("id")==1):
			sock.sendto("you hitted", (addr[0], addr[1]))
		elif (request.get("id")==2):
			sock.sendto("you stand", (addr[0], addr[1]))
		print ("received message:", request)
		
		
t = threading.Thread(target=server)
t.start()