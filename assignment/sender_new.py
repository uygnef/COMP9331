from socket import *
from select import *
import time
import sys, getopt
from random import *

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

def start(IP, port):
    ADDR = (IP, int(port))
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.sendto(segment(syn=1).seg, ADDR)  #syn=1, seq_num=0
    data,ADDR = sock.recvfrom(1024)
    seg = tr_seg(data)
    ack = seg.ack_num
    seq = seg.seq_num
    if ack == 1:
        seq += 1
        sock.sendto(segment(ack_num = seq).seg, ADDR)
        print("connect success")

    return sock,ADDR,0

def PLD_send(segment):
    global sock
    global ADDR
    #global log_file
    #log_file.write()
    if round(random() * possi):
        sock.sendto(segment.seg, ADDR)
        print("PLD_send:", segment.data, segment.seq_num)

def create_window():
    global have_send
    global file
    global sequence_number
    global data
    while len(have_send) < MWS and data:
        have_send.append(segment(data = str(data), seq_num = sequence_number))
        sequence_number += len(data)
        data = file.read(MSS)
    return data

def close(ADDR):
    global sock
    global sequence_number
    last_time = time.time()

    print("willlllll close")
    while True:
        sock.sendto(segment(seq_num=sequence_number + 2, fin=1).seg, ADDR)
        inf, outf, errf = select([sock, ], [], [])
        if inf:
            print("recv ack")
            se,ADDR = sock.recvfrom(1024)
            seg = tr_seg(se)
            print("compare:",seg.ack_num, sequence_number +3)
            if seg.ack_num == sequence_number +3:
                continue
            if seg.FIN == 1:
                sock.close()
                break

ops, args = getopt.getopt(sys.argv[1:], " ")

IP = args[0]
port = args[1]
read_file = args[2]
MWS_bit = int(args[3])
MSS = int(args[4])
MWS = MWS_bit // MSS
timeout= int(args[5])
possi = float(args[6])
seeds = int(args[7])
seed(seeds)
sock, ADDR, sequence_number = start(IP,port)
file = open(read_file)


have_send = []

timer = time.time()

old_ack = -1
fast_re = 0
data = file.read(MSS)
while create_window() or have_send:
    print("new loop")
    for i in have_send:
        inf, outf, errf = select([sock, ], [], [])
        if inf:
            s, ADDR = sock.recvfrom(1024)       #receive the data and react according ack_num
            seg = tr_seg(s)
            if old_ack == seg.ack_num:
                fast_re += 1
                old_ack = seg.ack_num
                if fast_re >= 3:
                    fast_re = 0
                    print("use fast retrans")
                    break
            for j in have_send:
                if seg.ack_num == j.seq_num+len(j.data):  # judge if the ack_num == last sequence number
                    print("have cutdown")
                    have_send = have_send[have_send.index(j)+1:]  # if the sequence number is in have_send, move the window
                    timer = time.time()                     #break to the beginning and send according new window
                    break
                                                            #if update the window, go to create_window.
        if time.time() > timer + timeout / 1000:        #if timeout, go to beginning and resend from the first
            #print("timer before:", timer)
            timer = time.time()                        #one in send window. reset timer.
            print("time out! timer = ", timer, "---",time.time())
            break
        PLD_send(i)
close(ADDR)
  
        

















