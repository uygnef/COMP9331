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
            graph[data[0]] = float(data[1])
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
keep_alive ={}

# data: node_name port_number distance
for lines in config_file:
    data = lines.split(" ")
    if not node_name in graph:
        graph[node_name] = {}
    if len(data) == 3:
        graph[node_name][data[0]] = float(data[1])
        node_port[data[0]] = int(data[2])
        keep_alive[int(data[2])] = 3
print(keep_alive)

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
    global keep_alive
    if inf:
        for sockets in inf:
            message, ADDR = sockets.recvfrom(1024)
            node, recv_graph = decode(message)
            # if node_name == 'E' or ADDR[1] == 2002:
            #     print("recv node and graph are ", node,recv_graph)
            keep_alive[ADDR[1]] = 3
            if node not in graph:
                graph[node] = recv_graph
            if node not in recv_from:
                recv_from[node] = [ADDR[1]]
            elif ADDR[1] not in recv_from[node]:
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
def Dijkstra_Algrm(graph):
    result_set = {}
    set_N = []
    from_to_list = {}
    inf = float("inf")
    self_graph = graph[node_name]
    for node in graph:
        if node_name != node:
            if node in self_graph:
                from_to_list[node] = node_name
                result_set[node] = graph[node_name][node]
            else:
                result_set[node] = inf

    # print("result set is", result_set)
    sorted_result_set = sorted(result_set.items(), key=lambda d: d[1])

    while len(set_N) < len(sorted_result_set):
        break_flag = False
        for node in sorted_result_set:
            if node[0] not in set_N:
                set_N.append(node[0])
                node_distance = node[1]
                for new_node in graph[node[0]]:
                    if new_node == node_name:
                        continue
                    if graph[node[0]][new_node] + node_distance < result_set[new_node]:
                        from_to_list[new_node] = node[0]
                        result_set[new_node] = graph[node[0]][new_node] + node_distance
                        break_flag = True
                if break_flag:
                    break
        sorted_result_set = sorted(result_set.items(), key=lambda d: d[1])
    return result_set, from_to_list
    # print(set_N, sorted_result_set,from_to_list)
    # print(node_name, result_set)

def delete_node(node):
    global node_port
    global graph
    global recv_from
    port = node_port[node]
    try:
        del node_port[node]
        del graph[node]
        del recv_from[node]
    except KeyError:
        pass
    for i in graph:
        for j in graph[i]:
            if j == node:
                del graph[i][j]
                break
    for i in recv_from:
        try:
            recv_from[i].remove(port)
        except ValueError:
            pass

recv_from = {node_name:[port_number]}
# print("Initial recv_from is", recv_from)
start_time = time.time()
now_time = time.time() - 1 #make sure it will start immediately at beginning
delete_list = []
while(time.time() <= start_time + 30):
    if node_name == 'D' and time.time() >= start_time +15:
        break
    if time.time() >= now_time + 1:
        for node in graph:
            # if node_name == 'W':
            #     print(node)
            broadcast(node)
        update_graph()
        #dealing with node failures
        for port in node_port:
            keep_alive[node_port[port]] -= 1
            if keep_alive[node_port[port]] <= 0:
                delete_list.append(port)
        while delete_list:
            delete_node(delete_list.pop())
        now_time = time.time()
        # if node_name == 'W':
        #     print("ccccc",node_name, graph)
print(node_name, graph)
sock.close()

graph = {'A': {'B': 2, 'D': 1, 'C': 5},
         'E': {'D': 1, 'F': 2, 'C': 1},
         'C': {'A': 5, 'E': 1, 'D': 3, 'F': 5, 'B': 3},
         'D': {'A': 1, 'C': 3, 'B': 2, 'E': 1},
         'F': {'C': 5, 'E': 2},
         'B': {'A': 2, 'D': 2, 'C': 3}}

def find_shortest_path(result_set, from_to_list):
    #result set A {'F': 4, 'C': 3, 'D': 1, 'E': 2, 'B': 2}
    #from_to_list {'F': 'E', 'C': 'E', 'D': 'A', 'E': 'D', 'B': 'A'}
    least_cost = {}
    for node in result_set:
        least_cost[node] = [node]
        next_node = from_to_list[node]
        while next_node != node_name:
            least_cost[node].append(next_node)
            next_node = from_to_list[next_node]
        least_cost[node].append(next_node)
        least_cost[node].reverse()
    for node in sorted(least_cost.keys()):
        path = ""
        for i in least_cost[node]:
            path += str(i)
        print("least-cost path to node %s: %s and the cost is %.1f"%(node, path, result_set[node]))
    return least_cost


result_set, from_to_list = Dijkstra_Algrm(graph)
least_cost_path = find_shortest_path(result_set, from_to_list)
