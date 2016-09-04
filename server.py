from socket import *
import socket, sys, getopt
ADDR = ('127.0.0.1', 31415)  
sock = socket.socket(AF_INET, SOCK_DGRAM)  
sock.bind(ADDR)  

for i in range(10):
	data,ADDR = sock.recvfrom(1024,ADDR) 
	print(data)
	sock.sendto("i".encode("UTF-8"),ADDR)