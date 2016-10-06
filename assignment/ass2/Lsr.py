import socket,sys, re

class packet:
    def __init__(self, node_name, port_number, distance):
        self.node_name = node_name
        self.port_number = port_number
        self.distance = distance

argv = sys.argv[1:]
node_name = argv[0]
port_number = int(argv[1])
config_file = open(argv[2])

address = ('localhost', port_number)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)

graph = {}
for lines in config_file:
    data = lines.split(" ")
    if len(data) == 3:
        graph[data[0]] = {'port':int(data[2]), 'cost':int(data[1])}

print(graph)


