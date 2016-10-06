import socket,sys, re

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

def encode(graph):
    message = node_name + "\n"
    for i in graph[node_name]:
        message += i + " " + str(graph[node_name][i]) + "\n"
    return message

def decode(message):
    msg_list = message.split("\n")
    graph = {}
    node_name = msg_list[0]
    for lines in msg_list[1:]:
        data = lines.split(" ")
        if len(data) == 2:
            graph[data[0]] = int(data[1])
    return node_name, graph

print(encode(graph))
n, m = decode(encode(graph))
print(n,m)

