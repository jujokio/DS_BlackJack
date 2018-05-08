import socket
import struct
import sys
import threading
import json
import time
import traceback

def getPlayer(sock):
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		request = json.loads(data.decode())
		print (addr)
		if (request.get("id")==0):#Join game
			return (addr[0], addr[1])

def sendMessageAndReceiveResponse(sock, ip, port, response):
	#send message to player
	sock.sendto(response, ( str(ip), int(port) ))
	# wait for response
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		request = json.loads(data.decode())
		print (addr)
		if addr[0] == ip and addr[1] == port:
			if (request.get("id")==0):#Join game
				if (request.get("status")=="success"):
					break
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
			elif (request.get("id")==6):
				if (request.get("status")=="success"):
					break
			print ("received message:", request)
		else:
			response={"id" : 4, "message" : "Not your turn"}
			sock.sendto(json.dumps(response).encode(), (addr[0], addr[1]))
	return response

def startTimer():
	traceback.print_exc(file=sys.stdout)
	print ("\n\n\n")
	gameTime=0
	print("called start timer")
	tim = threading.Thread(target=timer)
	tim.start()
	
	
def timer():
	print("timer thread!!!!!!!!!!!!!")
	global gameTime
	while True:
		time.sleep(1)
		if gameTime is None:
			print("create gametime pls thread!!!!!!!!!!!!!")
			gameTime =0
		gameTime += 1

if __name__ == "__main__":	
	#gameTime=0
	
	try:	
		t = threading.Thread(target=server)
		t.start()
		#startTimer()

	except KeyboardInterrupt:
			sys.exit(1)