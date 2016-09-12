from socket import *
from select import *
import sys, getopt

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

def start(port):
    ADDR = ('127.0.0.1', int(port))
    sock = socket(AF_INET, SOCK_DGRAM)  
    sock.bind(ADDR)
    data,ADDR = sock.recvfrom(1024)  
    seg = tr_seg(data)
    if seg.SYN == 1:
        sock.sendto(segment(syn=1, seq_num=0, ack_num=seg.seq_num+1, ack=1).seg, ADDR)
    data,ADDR = sock.recvfrom(1024)  
    seg = tr_seg(data)
    #print(seg)
    #ack = seg.ack_num
    if seg.ACK == 1:
        #print("connect success!")
        return sock,seg.seq_num, ADDR,1
    else:
        sock.close()
        exit("Fail to connect")
ops, args = getopt.getopt(sys.argv[1:], " ")
port = args[0]
file_name = args[1]
sock, ack, ADDR, sequence_number =start(port)
f=open(file_name,'w')
log_file = open("Receiver_log.txt", "w")
amount_of_data = 0
num_of_data = 0
duplicate_seg = 0

while True:
    inf, outf, errf = select([sock, ], [], [], 0)
    if inf != []:
        #print("no input")
       # send_seg = segment(ack_num = ack,seq_num=sequence_number)
       # sock.sendto(send_seg.seg, ADDR)
    #else:
        data,ADDR = sock.recvfrom(1024)
        seg = tr_seg(data)
        line = seg.data
        #log_file.writelines("rcv  A %8d %s %8d \n" % (seg.seq_num, seg.data, seg.ack_num))

        print(seg.seq_num)
        if seg.FIN == 1:
            sock.sendto(segment(ack_num=seg.seq_num+3, seq_num=sequence_number).seg, ADDR)
            sequence_number += 1
            sock.sendto(segment(fin=1, ack_num=seg.seq_num+4,seq_num=sequence_number).seg, ADDR)
            sock.close()
            #print("sock closed")
            break
        if ack == seg.seq_num:
            ack = seg.seq_num + len(line)
            f.write(line)
        else:
            duplicate_seg += 1

        num_of_data += 1        #write lines into log
        amount_of_data += len(seg.data.encode("UTF-8"))

        send_seg = segment(ack_num=ack, seq_num=sequence_number)
        sock.sendto(send_seg.seg, ADDR)
        #log_file.writelines("send  D %8d %s %8d \n" % (send_seg.seq_num, send_seg.data, send_seg.ack_num))


log_file.writelines("Amount of Data Received (in bytes):%d\n"%amount_of_data)
log_file.writelines("Number of Data Segments Received:%d\n"%num_of_data)
log_file.writelines("Number of duplicate segments received:%d\n"%duplicate_seg)



            
            
            
            
            
            
            
