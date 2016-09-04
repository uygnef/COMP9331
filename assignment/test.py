from socket import *
import socket, sys, getopt
def est():
	ADDR = ('localhost', 31415)
	sock = socket.socket(AF_INET, SOCK_DGRAM)
	sock.connect(ADDR)
	return sock
ADDR = ('localhost', 31415)
sock = est()
for i in range(10):
	sock.sendto("1".encode("UTF-8"),ADDR)
	data, ADDR = sock.recvfrom()
	print(data)
sock.sendto("1".encode("UTF-8"),ADDR)
