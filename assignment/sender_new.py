from socket import *
from select import *
import time
import sys, getopt
from random import *

class segment:  # use segment class to store the sending segment.
    def __init__(self, syn=0, ack=0, fin=0, seq_num=0, ack_num=0, data=""):
        self.SYN = syn
        self.FIN = fin
        self.ACK = ack
        self.ack_num = ack_num  # new sequence number, sender as ack number
        self.seq_num = seq_num  # new sequence number
        self.data = data
        self.seg_str = str(self.SYN) + str(self.FIN) + str(self.ACK)\
                       + "{0:08d}".format(self.seq_num) \
                       + "{0:08d}".format(self.ack_num) + data
        self.seg = self.seg_str.encode("UTF-8")

    def __repr__(self):
        print("seg_str", self.seg_str)
        print("SYN", self.SYN)
        print("FIN", self.FIN)
        print("ACK", self.ACK)
        print("seq_num", self.seq_num)
        print("ack_num", self.ack_num)
        print("data", self.data)
        return ("--------------------")

def tr_seg(data):       #translate segment into class
    seg_str = data.decode("UTF-8")
    self = segment(syn = int(seg_str[0]),fin = int(seg_str[1]), ack = int(seg_str[2]),
                    seq_num = int(seg_str[3:11]),
                    ack_num = int(seg_str[11:19]), data = seg_str[19:])
    return self

def start(IP, port):
    global log_file
    ADDR = (IP, int(port))
    sock = socket(AF_INET, SOCK_DGRAM)
    seq = 0
    first_segment = segment(syn=1,seq_num=seq)
    sock.sendto(first_segment.seg, ADDR)  #syn=1, seq_num=0
    log_file.writelines("snd  %2.3f S %8d %3d %8d\n"%( time.time()%60, first_segment.seq_num, len(first_segment.data), 0 ))

    data,ADDR = sock.recvfrom(1024)
    seg = tr_seg(data)
    log_file.writelines("rcv  %2.3f SA%8d %3d %8d\n"%( time.time()%60, seg.seq_num, len(seg.data), seg.ack_num ))

    if seg.SYN == 1 and seg.ACK ==1:
        seq += 1
        sock.sendto(segment(ack=1, ack_num = seg.seq_num+1, seq_num=seq).seg, ADDR)
        log_file.writelines("snd  %2.3f A %8d %3d %8d\n" % (time.time() % 60, seq, 0, seg.seq_num+1))
        #print("connect success")
    else:
        sock.close()
        exit("connect fail")
    return sock,ADDR,seq,seg.seq_num+1

def PLD_send(segment):
    global sock
    global ADDR
    global log_file
    global data_seg_sd
    global data_drop
    #global send_segment
    #global drop_segment
    if random()+possi < 1:
        sock.sendto(segment.seg, ADDR)
        data_seg_sd += 1
        #print("PLD_send:", segment.data, segment.seq_num)
        log_file.writelines("snd  %2.3f D %8d %3d %8d\n" % (time.time() % 60, segment.seq_num, len(segment.data), segment.ack_num))
    else:
        data_drop += 1
        log_file.writelines("drop %2.3f D %8d %3d %8d\n"%( time.time()%60, segment.seq_num, len(segment.data), segment.ack_num))
    global amount_data_tr
    amount_data_tr += len(segment.data.encode("utf-8"))



def create_window():
    global send_window
    global file
    global sequence_number
    global acknowledge_number
    global data
    while len(send_window) < MWS and data:
        send_window.append(segment(data = str(data), seq_num = sequence_number, ack_num=acknowledge_number))
        sequence_number += len(data)
        data = file.read(MSS)
    return data

def close(ADDR):
    global sock
    global sequence_number

    #print("willlllll close")
    sock.sendto(segment(seq_num=sequence_number + 2, fin=1).seg, ADDR)
    log_file.writelines("snd  %2.3f F %8d %3d %8d\n" % (time.time() % 60, sequence_number+2, 0, acknowledge_number))
    #print("recv ack")
    while True:
        se,ADDR = sock.recvfrom(1024)
        seg = tr_seg(se)
        if seg.FIN == 1:
            log_file.writelines("rcv  %2.3f FA%8d %3d %8d\n" % (time.time() % 60, seg.seq_num, 0, seg.ack_num))
                    #sock.sendto(segment(ack=1), ADDR)
            log_file.writelines("snd  %2.3f A %8d %3d %8d\n" % (time.time() % 60, seg.ack_num, 0, seg.seq_num+1))
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
amount_data_tr = 0
data_seg_sd = 0
data_drop = 0
file = open(read_file)
log_file = open("Sender_log.txt", "w")
sock, ADDR, sequence_number,acknowledge_number = start(IP,port)
number_of_dup = 0
privious_seq = 0
send_window = []

timer = time.time()

last_ack = -1
fast_re = 0
data = file.read(MSS)
create_window()
bb = 0
start_time = time.time()
while send_window:
    all_send_flag = False
    for i in send_window:
        try:            #wired error, try to start from first element in send_window
            send_window.index(i)
        except ValueError:
            break
        PLD_send(i)
        inf, outf, errf = select([sock,], [], [], 0)
        #print(inf[-1].recvfrom(1024))
        recv_flag = False
        while True:              #try to get the last acknowledge number
            inf, outf, errf = select([sock, ], [], [], 0)
            if inf:
                recv_segment, ADDR = inf[-1].recvfrom(1024)
                recv_flag = True
            else:
                break

        if recv_flag:                  #receive the data and react according ack_num
            seg = tr_seg(recv_segment)
            log_file.writelines("rcv  %2.3f A %8d %3d %8d \n" % (time.time()%60, seg.seq_num, len(seg.data), seg.ack_num))

            if last_ack == seg.ack_num:
                number_of_dup += 1
                fast_re += 1
                last_ack = seg.ack_num
                if fast_re >= 3:    # fast retrans
                    fast_re = 0
                    break

            last_ack = seg.ack_num
            for j in send_window:
                if seg.ack_num == j.seq_num+len(j.data):  # judge if the ack_num == last sequence number
                    send_window = send_window[send_window.index(j)+1:]  # if the sequence number is in send_window, move the window
                    create_window()
                    timer = time.time()                     #break to the beginning and send according new window
                    break
                                                            #if update the window, go to create_window.
        if time.time() > timer + timeout / 1000:        #if timeout, go to beginning and resend from the first
            break

        if send_window:         #judge if send all data in send_window
            if i == send_window[-1]:
                all_send_flag = True
    while all_send_flag and time.time() < timer + timeout / 1000:
        #print("timeout!")
        pass
    timer = time.time()

close(ADDR)
end_time = time.time()
print("all time:", end_time - start_time)
log_file.writelines("Amount of Data Transferred (in bytes):%d\n"%amount_data_tr)
log_file.writelines("Number of Data Segments Sent (excluding retransmissions):%d\n"%data_seg_sd)
log_file.writelines("Number of Packets Dropped  (by the PLD module):%d\n"%data_drop)
log_file.writelines("Number of Duplicate Acknowledgements received:%d\n"%number_of_dup)

