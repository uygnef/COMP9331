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

##sock.settimeout(1)
#receive socket established
##receive_addr = ('localhost',31000)
##recv_sock = socket.socket(AF_INET, SOCK_DGRAM)  
##recv_sock.connect(receive_addr)

# MMS = 64
# def estb_connect(ADDR):				#establishe the connection (three-way handshake)
#     sock = socket.socket(AF_INET, SOCK_DGRAM)
#     SYN_SEG, seq = create_seg(SYN=1, seq_num=0)	#creat SYN segment.
#     sock.sendto(SYN_SEG,ADDR)
#     try(data, sender_add = sock.recvfrom(1024))
#         data = data.decode("UTF-8")
#         if data[1:2] == "11" and int(data[11:19])+1 == seq+1:
#             seq += 1
#             SYN_SEG, seq = create_segment(SYN=1, seq_num = seq)

			
class segment:          #use segment class to store the sending segment.
    def __init__(self, syn=0, fin=0, seq_num=0, ack_num=0, data=""):
        self.SYN = syn
        self.FIN = fin
        self.ack_num = ack_num     #new sequence number, sender as ack number
        self.seq_num = seq_num                      #new sequence number
        self.data = data
        self.seg_str =  str(self.SYN)+str(fin)\
                         + "{0:08d}".format(self.seq_num)\
                         +"{0:08d}".format(self.ack_num)+ data
        self.seg = self.seg_str.encode("UTF-8")

    def tr_seg(self, data):
        seg_str = data.decode("UTF-8")
        self.SYN = int(seg_str[0])
        self.FIN = int(seg_str[1])
        self.seq_num = int(seg_str[3:10])
        self.ack_num = int(seg_str[10:18])
        if len(seg_str) > 18:
            self.data = seg_str[18:]
        else:
            self.data = ""

    def __repr__(self):
        print("seg_str", self.seg_str)
        print("SYN", self.SYN)
        print("FIN", self.FIN)
        print("seq_num",self.seq_num)
        print("ack_num",self.ack_num)
        print("data", self.data)
        return("--------------------")

def sequence_check(rcv,send):           #check whether the sequence and ack number
    if rcv.ack_num != send.seq_num + len(send.data): #are correct.
        return False
    return True

ADDR = ('localhost', 31415)
sock = socket(AF_INET, SOCK_DGRAM)

sock.sendto("1".encode("UTF-8"),ADDR)
sock.sendto("2".encode("UTF-8"),ADDR)
data,ADDR = sock.recvfrom(1024)
print(data)
sock.sendto("3".encode("UTF-8"),ADDR)
data,ADDR = sock.recvfrom(1024)
print(data)
data,ADDR = sock.recvfrom(1024)
print(data)


        
