from socket import *
from queue import *
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

def start():
    ADDR = ('localhost', 31415)
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
    if round(random() * possi):
        sock.sendto(segment.seg, ADDR)
        #print(segment(data = str(data), seq_num = seq))

def create_window():
    global have_send
    global file
    global sequence_number
    global MWS
    global data
    while len(have_send) < MWS:
        have_send.append(segment(data = str(data), seq_num = sequence_number))
        sequence_number += len(data)
        data = file.read(32)
    if data:
        return True
    return False

sock, ADDR, sequence_number = start()
file = open('test1.txt')
seed(50)
possi = 1
have_send = []
MWS = 3
timer = time.time()

while create_window():
    for i in have_send:
        if time.time() < timer + timeout / 1000 or fast_flag == 3:
            timer == time.time()
            break
        inf, outf, errf = select([sock, ], [], [], timeout/1000)
        if inf != []:
            s, ADDR = sock.recvfrom(1024)       #receive the data and react according ack_num
            seg = tr_seg(s)
            #print(seg, "seq_num =", seq)
            for i in have_send:
                if seg.ack_num == i.seq_num:  # judge if the ack_num == last sequence number
                    have_send = have_send[have_send.index(i):]    #if the sequence number is in have_send, move the window
                    timer = time.time()
                    break
        else:
            PLD_send(i)






        PLD_send(i)



while data or len(have_send):
    if len(have_send) < MWS and data:
        flag = round(random()*possi)
        send_seg = PLD_send(sock, data, seq, ADDR, flag)
        have_send.append(send_seg)

        inf, outf, errf = select([sock, ], [], [])
        if inf != []:
            s, ADDR = sock.recvfrom(1024)       #receive the data and react according ack_num
            seg = tr_seg(s)
            #print(seg, "seq_num =", seq)
            for i in have_send:
                if seg.ack_num == i.seq_num:  # judge if the ack_num == last sequence number
                    have_send = have_send[have_send.index(i):]    #if the sequence number is in have_send, move the window

        data = file.read(32)
        seq += len(data)
    else:
        while len(have_send) >= MWS or (not data and len(have_send) != 0):
            for a in have_send:
                inf, outf, errf = select([sock, ], [], [])
                if inf != []:
                    s, ADDR = sock.recvfrom(1024)  # receive the data and react according ack_num
                    seg = tr_seg(s)
                    print("ack_num =", seg.ack_num)
                    for i in have_send:
                        if seg.ack_num == i.seq_num +len(i.data):  # judge if the ack_num == last sequence number
                            have_send = have_send[have_send.index(i)+1:]

                    break
                flag = round(random() * possi)
                send_seg = PLD_send(sock, a.data, a.seq_num, ADDR, flag)

                print(send_seg.seq_num, len(have_send), have_send[0].data)
  
        

















