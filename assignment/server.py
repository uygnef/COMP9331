from socket import *
import socket, sys, getopt
ADDR = ('127.0.0.1', 31415)  
sock = socket.socket(AF_INET, SOCK_DGRAM)  
sock.bind(ADDR)  

for i in range(10):
	data = sock.recv(1024) 
	print(data)
	sock.sendto(ADDR, "113".encode("UTF-8"))