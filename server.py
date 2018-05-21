import socket
import struct
import sys
import threading
import json
import time
import traceback
from Crypto.Cipher import AES
import base64

global gameTime
global timeOut
gameTime = 0
timeOut =False


MASTER_KEY="NoName_WELCOMETODISTRIBUTEDFUCKFEST"
def cypher_aes(msg_text, encrypt=True, secret_key=MASTER_KEY):
    # an AES key must be either 16, 24, or 32 bytes long
    # in this case we make sure the key is 32 bytes long by adding padding and/or slicing if necessary
    remainder = len(secret_key) % 16
    modified_key = secret_key.ljust(len(secret_key) + (16 - remainder))[:32]
    print(modified_key)

    # input strings must be a multiple of 16 in length
    # we achieve this by adding padding if necessary
    remainder = len(msg_text) % 16
    modified_text = msg_text.ljust(len(msg_text) + (16 - remainder))
    print(modified_text)

    cipher = AES.new(modified_key, AES.MODE_ECB)  # use of ECB mode in enterprise environments is very much frowned upon

    if encrypt:
        return base64.b64encode(cipher.encrypt(modified_text)).strip()

    return cipher.decrypt(base64.b64decode(modified_text)).strip()
def encrypt_val(clear_text):    
    return cypher_aes(clear_text,True)

def decrypt_val(text):
    temp = cypher_aes(text,False)
    temp = temp.strip('\0'.encode())
    return temp
	





def getPlayer(sock):
	global gameTime
	global timeOut

	sock.settimeout(20)
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	data=decrypt_val(data)
	print("\n\n", data)
	request = json.loads(data)
	if (request.get("id")==0):#Join game
		return (addr[0], addr[1])
	

def sendMessageAndReceiveResponse(sock, ip, port, response):
	#send message to player
	sock.sendto(response, ( str(ip), int(port) ))
	# wait for response
	#while True:
	sock.settimeout(30)
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	request = json.loads(data.decode())
	request = decrypt(request)
	if addr[0] == ip and addr[1] == port:
		if (request.get("id")==0):#Join game
			if (request.get("status")=="success"):
				return
		elif (request.get("id")==1):
			response={"id" : 1, "message" : "you hitted"}
			response = encrypt_val(response)
			sock.sendto(json.dumps(response).encode(), (addr[0], addr[1]))
			
		elif (request.get("id")==2):
			response={"id" : 2, "message" : "you stand"}
			response = encrypt_val(response)
			sock.sendto(json.dumps(response).encode(), (addr[0], addr[1]))
			
		elif (request.get("id")==3):
			response={"id" : 3, "message" : "you quit"}
			response = encrypt_val(response)
			sock.sendto(json.dumps(response).encode(), (addr[0], addr[1]))
			
		elif (request.get("id")==6):
			if (request.get("status")=="success"):
				return
		print ("received message:", request)
	else:
		response={"id" : 4, "message" : "Not your turn"}
		response = encrypt_val(response)
		sock.sendto(json.dumps(response).encode(), (addr[0], addr[1]))
	return response

def startTimer():
	print ("startTimer\n\n\n")
	global gameTime
	global timeOut	
	print (gameTime, timeOut)
	tim = threading.Thread(target=timer)
	tim.start()
	
	
def timer():
	print ("timer thread\n\n\n")
	global gameTime
	global timeOut
	while True:
		time.sleep(1)
		if gameTime >= 9:
			print("10 sec TimeOut called!")
			timeOut = True
			gameTime=0
		elif (gameTime >= 5 and timeOut):
			print("timeout reset")
			timeOut = False
			gameTime=0
		
		gameTime += 1

if __name__ == "__main__":	
	#gameTime=0
	
	try:	
		t = threading.Thread(target=server)
		t.start()
		#startTimer()

	except KeyboardInterrupt:
			sys.exit(1)