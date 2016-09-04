from socket import *
import sys, getopt
import time

def create_segment(SYN=0, FIN=0, ACK=0, seq_num=0, ack_num=0, data=""):   #creat data segments
    string = str(SYN)+str(FIN)+ str(ACK)+ "{0:08d}".format(seq_num)+"{0:08d}".format(ack_num)+str(data.decode("UTF-8"))
    return string.encode("UTF-8")

ADDR = ('127.0.0.1', 31415)  
sock = socket(AF_INET, SOCK_DGRAM)  
sock.bind(ADDR)  

segment, sdr_add = sock.recvfrom(1024)
data = segment.decode("UTF-8")
if data == "1":
    sock.sendto("101".encode("UTF-8"), sdr_add)
else:
    print("Fail to establish the connection")
    sock.close()
    exit(1)

segment, sdr_add = sock.recvfrom(1024)
data = segment.decode("UTF-8")
for i in range(10):
    print(i)
    data,sdr_add = sock.recvfrom(1024)
    print(data)
    sock.sendto("1".encode("UTF-8"), sdr_add)
##if data != "001":
##    print("Fail to establish the connection")
##    sock.close()
##    exit(1)

##while data != :  
##    data, sdr_add  = sock.recvfrom(1024)
##    
##if data == "0".encode("UTF-8"):
##    sock.sendto("01".encode("UTF-8"), sdr_add)



