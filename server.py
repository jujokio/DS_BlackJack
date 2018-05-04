import socket
import struct
import sys
import threading
import json

from objects import BlackJackObject

def server(sock):
	
	while True:
		players=0
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		request = json.loads(data.decode())
		print (addr)
		if (request.get("id")==0):#Join game
			if (players<=2):
				response={"id" : 0, "message" : "success"}
				sock.sendto(json.dumps(response).encode(), (addr[0], addr[1]))
				return (addr[0], addr[1])
		elif (request.get("id")==1):
			response={"id" : 1, "message" : "you hitted"}
			sock.sendto(json.dumps(response).encode(), (addr[0], addr[1]))
			break
		elif (request.get("id")==2):
			response={"id" : 2, "message" : "you stand"}
			sock.sendto(json.dumps(response).encode(), (addr[0], addr[1]))
			break
		elif (request.get("id")==3):
			response={"id" : 3, "message" : "you quit"}
			sock.sendto(json.dumps(response).encode(), (addr[0], addr[1]))
			break
		print ("received message:", request)
	return response
		
if __name__ == "__main__":	
	try:	
		t = threading.Thread(target=server)
		t.start()
	except KeyboardInterrupt:
			sys.exit(1)