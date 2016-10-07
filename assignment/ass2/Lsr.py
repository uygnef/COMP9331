import socket,sys, select, time, heapq

def encode(node_name,node_graph):
    message = node_name + "\n"
    for i in node_graph:
        message += i + " " + str(node_graph[i]) + "\n"
    return message.encode("UTF-8")

def decode(message):
    #print("message is", message)
    msg_list = (message.decode("UTF-8")).split("\n")
    graph = {}
    node_name = msg_list[0]
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
            # if node_name == 'E' or ADDR[1] == 2002:
            #     print("recv node and graph are ", node,recv_graph)
            if node not in graph:
                graph[node] = recv_graph
            if node not in recv_from:
                recv_from[node] = [ADDR[1]]
            else:
                recv_from[node].append(ADDR[1])

#def timer(port, node, send_graph)
def broadcast(node):
    for neighbour_node in node_port:    #对于所有的相邻节点，
        port = node_port[neighbour_node]  # 对此相邻的节点发送
        if node not in recv_from or port not in recv_from[node]:#如果接受的图对应的节点B不在  recv_from中 对应的节点B 的记录里
            # if node_name == 'C' and neighbour_node == 'A':
            #     print("send node is C to A", node)
            #     print("recv_form is", recv_from)
            sock.sendto(encode(node, graph[node]), ("localhost", port))

recv_from = {node_name:[port_number]}
# print("Initial recv_from is", recv_from)
start_time = time.time()
now_time = time.time() - 1 #make sure it will start immediately at beginning
# while(time.time() <= start_time + 30):
#     if time.time() >= now_time + 1:
#         for node in graph:
#             # if node_name == 'W':
#             #     print(node)
#             broadcast(node)
#         update_graph()
#         now_time = time.time()
#         # if node_name == 'W':
#         #     print("ccccc",node_name, graph)
# print(node_name, graph)
sock.close()

graph = {'A': {'B': 2, 'D': 1, 'C': 5}, 'E': {'D': 1, 'F': 2, 'C': 1}, 'C': {'A': 5, 'E': 1, 'D': 3, 'F': 5, 'B': 3}, 'D': {'A': 1, 'C': 3, 'B': 2, 'E': 1}, 'F': {'C': 5, 'E': 2}, 'B': {'A': 2, 'D': 2, 'C': 3}}
def Dijkstra_Algrm(graph):
    result_set = {}
    inf = float("inf")
    self_graph = graph[node_name]
    for node in graph:
        if node_name != node:
            if node in self_graph:
                result_set[node] = graph[node_name][node]
            else:
                result_set[node] = inf
    result_set = sorted(result_set.items(), key=lambda d: d[1])
    if result_set:
        select_node = result_set[0]
        result_set = result_set[1:]
    print(node_name, result_set)

Dijkstra_Algrm(graph)