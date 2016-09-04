from socket import *
import sys, getopt
import time

ops, args = getopt.getopt(sys.argv[1:], " ")
if len(args) != 2:
    print("Input error")
    exit()
PORT = args[1]
HOST = args[0]

sock = socket(AF_INET, SOCK_STREAM)

sock.connect((HOST, PORT))
result = []
for _ in range(10):
    sock.send(''.encode("UTF-8"))
    start_time = time.time()
    try:
        sock.settimeout(1)
    except TimeoutError:
        continue

    received = sock.recv(1024).encode("UTF-8")
    end_time = time.time()
    rtt = end_time - start_time
    if received:
        print("pint to {}, seq = {}, rtt = {}ms".format(HOST, _,rtt))
    else:
        print("NO Connection")

