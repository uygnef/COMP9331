from socket import *
from queue import *
from select import *
import sys, getopt
from time import *
##ops, args = getopt.getopt(sys.argv[1:], " ")
##if len(args) != 2:
##    print("Input error")
##    exit()
##PORT = args[1]
##HOST = args[0]
# send socket established
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
    self = segment()
    seg_str = data.decode("UTF-8")
    self.SYN = int(seg_str[0])
    self.FIN = int(seg_str[1])
    self.seq_num = int(seg_str[2:10])
    self.ack_num = int(seg_str[10:18])
    if len(seg_str) > 18:
        self.data = seg_str[17:]
    else:
        self.data = ""
    return self
def sequence_check(rcv, send):  # check whether the sequence and ack number
    if rcv.ack_num != send.seq_num + len(send.data):  # are correct.
        return False
    return True
def start():
    ADDR = ('localhost', 31415)
    sock = socket(AF_INET, SOCK_DGRAM)
    SYN = segment(syn=1)
    sock.sendto(SYN.seg, ADDR)
    # receive data from sever
    recv_segment = segment()
    data, ADDR = sock.recvfrom(20)
    recv_segment.tr_seg(data)  # translate segment to the data class
    print(recv_segment)4    if not (recv_segment.ack_num == 1 and recv_segment.SYN == 1):  # first hand shake
        exit("connect error")

    # second hand shake
    sock.sendto(segment(seq_num=recv_segment.ack_num, ack_num=recv_segment.seq_num + 1).seg, ADDR)
    recv_segment = segment()
    data, ADDR = sock.recvfrom(1024)
    recv_segment.tr_seg(data)
    if not (recv_segment.ack_num == 1 and recv_segment.SYN == 1):
        exit("connect error")
    sock.sendto(segment(seq_num=1, ack_num=1).seg, ADDR)
    print("connect successful!"
    return seq_num, ack_num, sock
ack_repeat = 0  #record ack repeat times
last_ACK = 0

def read_reply(segment, window):    #read reply form receiver
    ACK = tr_seg(segment)   #and react according ACK number
    global ack_repeat
    global last_ACK
    if ACK == last_ACK:
        ack_repeat += 1
    if ack_repeat == 3:
        sock.sendto(seg[ACK], ADDR) #resend (fast retrans)

    while ACK > last_ACK and not window.empty():
        window.get() #window is a queue which store the sended segments
    while not window.full():
        window.put(file.read(32))
    return window

seq_num, ack_num, sock = start()
maxsize = 10
window = Queue(maxsize)  # creat a queue to store timer and sequence number
file = open('test1.txt')
data = file.read(32)
seg = segment(seq_num=seq_num, data=data, ack_num=ack_num)

due_time = 100
due = int(time()) + due_time
while data:
    inf, outf, errf = select([sock, ], [], [])
    if time() == due:
        re_trs(list)
    if inf:
        seg, ADDR = sock.recvfrom(1024)
        can_send = change_window(seg)  # compare the recv ack number with the window, update the window
    if can_send:
        sock.sendto(data, ADDR)

    due = time()
    window.put((seq_num, seq_num + len(seg.seg), due))  # seq_num, ack_num, due time

    recv, ADDR = sock.recvfrom(1024)
    recv_seg = segment()
    recv.tr_seg(recv)
    ack_num = recv_seg.seq_num

    data = file.read(32)
    seg = segment(data=data)

#
# sock.sendto("0".encode("UTF-8"), ADDR)
# data, recv_add = sock.recvfrom(1024)
# print(data)


