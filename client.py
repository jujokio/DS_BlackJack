import socket
import struct
import threading

UDP_IP = "127.0.0.1"
UDP_PORT_SERVER = 5005
MESSAGE = "Hello, World!"
UDP_PORT = 5006
def server():
	UDP_IP = "127.0.0.1"
	UDP_PORT = 5006
	global sock
	global response
	sock.settimeout(100)
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		data = struct.unpack("ii",data)
		#join game response, 1=success
		if (data[0]==0):
			if (data[1]==1):
				print "Liityit peliin"
			else:
				print "Full game or no work"
				joinGame()
		print "received message:", data

UDP_PORT=int(raw_input("ana portti"))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
t = threading.Thread(target=server)
t.start()
print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT_SERVER
print "message:", MESSAGE

def joinGame():
	server_ip=raw_input("Anna palvelimen IP osoite: ")
	server_ip='127.0.0.1'
	print "Joining game"
	print "--------------------------"
	request = ""
	request += struct.pack("i",0)# 0 = join game request
	try:
		sock.sendto(request, (server_ip, UDP_PORT_SERVER))
	except:
		joinGame()
		
response=""
joinGame()
#message = ""
#message += struct.pack("i",4)
#message += struct.pack("i",3)
#sock.sendto(message, (UDP_IP, UDP_PORT_SERVER))