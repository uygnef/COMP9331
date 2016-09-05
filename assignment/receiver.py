from socket import *
from queue import *
from select import *
import sys, getopt
from time import *

class segment:  # use segment class to store the sending segment.
    def __init__(self, syn=0, fin=0, seq_num=0, ack_num=0, data=""):
        self.SYN = syn
        self.FIN = fin
        self.ack_num = ack_num  # new sequence number, sender as ack number
        self.seq_num = seq_num  # new sequence number
        self.data = data
        self.seg_str = str(self.SYN) + str(fin) \
                       + "{0:08d}".format(self.seq_num) \
                       + "{0:08d}".format(self.ack_num) + data
        self.seg = self.seg_str.encode("UTF-8")

    def __repr__(self):
        print("seg_str", self.seg_str)
        print("SYN", self.SYN)
        print("FIN", self.FIN)
        print("seq_num", self.seq_num)
        print("ack_num", self.ack_num)
        print("data", self.data)
        return ("--------------------")
 
def tr_seg(data):       #translate segment into class
    seg_str = data.decode("UTF-8")
    if len(seg_str) > 18:
        se_data = seg_str[18:]
    else:
        se_data = ""
    self = segment(syn = int(seg_str[0]),fin = int(seg_str[1]),
                    seq_num = int(seg_str[2:10]),
                    ack_num = int(seg_str[10:18]), data = se_data)
    return self

def start():
    ADDR = ('127.0.0.1', 31415)  
    sock = socket(AF_INET, SOCK_DGRAM)  
    sock.bind(ADDR)
    data,ADDR = sock.recvfrom(1024)  
    seg = tr_seg(data)
    ack = seg.ack_num
    if seg.SYN == 1:
         sock.sendto(segment(seq_num=0, ack_num=ack+1).seg, ADDR)
    data,ADDR = sock.recvfrom(1024)  
    ack = tr_seg(data).ack_num
    #ack = seg.ack_num
    if ack == 1:
        print("connect success!")
        return sock,0, ADDR
    else:
        print("Fail to connect")
        return 0

sock, ack, ADDR=start()
print("ack=",ack)

while True:
    inf, outf, errf = select([sock, ], [], [], 0.1)
    if inf == []:
        send_seg = segment(ack_num = ack)
        sock.sendto(send_seg.seg, ADDR)

    else:
        data,ADDR = sock.recvfrom(2048)
        seg = tr_seg(data)
        line = seg.data

        if ack == seg.seq_num:
            ack = seg.seq_num + len(line)
            print(line, seg.seq_num)

        send_seg = segment(ack_num=ack)
        sock.sendto(send_seg.seg, ADDR)


            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            


