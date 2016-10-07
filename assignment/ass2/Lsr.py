import socket,sys, select, time
def encode(node_graph):
    message = node_name + "\n"
    for i in node_graph:
        message += i + " " + str(node_graph[i]) + "\n"
    return message.encode("UTF-8")

def decode(message):
    print("message is", message)
    msg_list = (message.decode("UTF-8")).split("\n")
    graph = {}
    node_name = msg_list[0]
    print(msg_list)
    for lines in msg_list[1:]:
        data = lines.split(" ")
        if len(data) == 2:
            graph[data[0]] = int(data[1])
    return node_name, graph
argv = sys.argv[1:]
node_name = argv[0]
port_number = int(argv[1])
config_file = open(argv[2])

address = ('localhost', port_number)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)
graph = {}
node_port = {}
# data: node_name port_number distance
for lines in config_file:
    data = lines.split(" ")
    if not node_name in graph:
        graph[node_name] = {}
    if len(data) == 3:
        graph[node_name][data[0]] = int(data[1])
        node_port[data[0]] = int(data[2])

'''
the recv_from is a dictionary.
 key is name of the node whose neighbour graph is send as message
 value is the name of the node which send that message.
 { neighbour graph of A : receive from {B, C, D}}
'''
def update_graph():
    global recv_from
    global graph
    inf, outf, errf = select.select([sock, ], [], [], 0)
    if inf:
        for sockets in inf:
            message, ADDR = sockets.recvfrom(1024)
            node, recv_graph = decode(message)
            if node not in graph:
                graph[node] = recv_graph
            if not node in recv_from:
                recv_from[node] = [ADDR[1]]
            else:
                recv_from[node].append(ADDR[1])

#def timer(port, node, send_graph)
def broadcast(node):
    for neighbour_node in node_port:    #对于所有的相邻节点，
        if node not in recv_from or neighbour_node not in recv_from[node]:#如果接受的图对应的节点B不在  recv_from中 对应的节点B 的记录里
            port = node_port[neighbour_node]    #对此相邻的节点发送
            sock.sendto(encode(graph[node]), ("localhost", port))

recv_from = {node_name:[node_name]}
start_time = time.time()
now_time = time.time() - 1 #make sure it will start immediately at beginning
while(time.time() <= start_time + 10):
    if time.time() >= now_time + 1:
        for node in graph:
            broadcast(node)
        update_graph()
        now_time = time.time()
        print(graph)


