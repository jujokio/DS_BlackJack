import socket
import struct
import sys
import threading

def server():
	UDP_IP = "127.0.0.1"
	UDP_PORT = 5005

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))
	players=0
	sock.settimeout(200)
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		data = struct.unpack("i",data)
		#Join game
		print addr
		if (data[0]==0):
			if (players<=2):
				response = ""
				response += struct.pack("i",0)# 0 = join game request
				response += struct.pack("i",0)# 0 = join game request
				sock.sendto(response, (addr[0], addr[1]))
		elif (data[0]==1):
			sock.sendto("you hitted", (addr[0], addr[1]))
		elif (data[0]==2):
			sock.sendto("you stand", (addr[0], addr[1]))
		print "received message:", data
		
		
t = threading.Thread(target=server)
t.start()