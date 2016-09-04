from socket import *
import sys, getopt
import time

##ops, args = getopt.getopt(sys.argv[1:], " ")
##if len(args) != 2:
##    print("Input error")
##    exit()
##PORT = args[1]
##HOST = args[0]
#send socket established
ADDR = ('localhost', 31415)
sock = socket(AF_INET, SOCK_DGRAM)
##sock.settimeout(1)
#receive socket established
##receive_addr = ('localhost',31000)
##recv_sock = socket.socket(AF_INET, SOCK_DGRAM)  
##recv_sock.connect(receive_addr)
sock.connect(ADDR)
def create_segment(SYN=0, FIN=0, ACK=0, seq_num=0, ack_num=0, data=""):   #creat data segments
    string = str(SYN)+str(FIN)+ str(ACK)+ "{0:08d}".format(seq_num)+"{0:08d}".format(ack_num)+str(data.decode("UTF-8"))
    return string.encode("UTF-8")

sock.sendto("1".encode("UTF-8"),ADDR)
if sock.recvfrom(1024)[0] != "101".encode("UTF-8"):
    print("Fail to establish the connection")
    exit(1)
sock.sendto("001".encode("UTF-8"))

file = open('test1.txt')
word = file.read(32).encode("UTF-8")
while word:
    segment = create_segment(data=word)
    sock.sendto(segment, ADDR)
    word = file.read(32)
    
    
    
sock.sendto("0".encode("UTF-8"), ADDR)
data, recv_add = sock.recvfrom(1024)
print(data)

        
