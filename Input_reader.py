# Function that returns two python dictionnaries : evac_paths & arcs
def parse_instance(path):

    evac_paths = {}  # {node_id : {'pop', 'max_rate', 'route_length', 'route_nodes':[node1,node2,..]} }
    arcs = {}        # arcs = {(node1,node2):{'duedate', 'length', 'capacity'}}

    myfile = open(path, 'r')
    ins = myfile.readlines()
    i = 0
    state = 0

    while i < len(ins):
        l = ins[i]
        l = l.split(" ")

        if l[0] == 'c':
            i = i + 1

        elif state == 0:
            num_evac_nodes = int(l[0])
            # safe_node = int(l[1]) UNUSED RIGHT NOW, MAY BE USEFUL LATER

            for j in range(0, num_evac_nodes):
                i = i + 1
                l = ins[i]
                l = l.split(" ")
                node_id = int(l[0])  # id of node
                pop = int(l[1])  # population
                max_rate = int(l[2])  # max rate
                route_length = int(l[3])  # k : length of route
                route_nodes = []  # escape route nodes init as empty set

                for k in range(0, int(l[3])):
                    route_nodes.append(int(l[4 + k]))

                evac_paths[node_id] = {'pop': pop, 'max_rate': max_rate, 'route_length': route_length,
                                       'route_nodes': route_nodes}

            i = i + 1
            state = 1

        elif state == 1:
            # num_nodes = int(l[0]) UNUSED RIGHT NOW, MAY BE USEFUL LATER
            num_arcs = int(l[1])

            for j in range(0, num_arcs):
                i = i + 1
                l = ins[i]
                l = l.split(" ")
                node1 = int(l[0])
                node2 = int(l[1])
                duedate = int(l[2])
                length = int(l[3])
                capacity = int(l[4])

                if node1 < node2:
                    arcs[(node1, node2)] = {'due_date': duedate, 'length': length, 'capacity': capacity}
                else:
                    arcs[(node2, node1)] = {'due_date': duedate, 'length': length, 'capacity': capacity}

            state = -1

        else:
            i = i + 1

    return evac_paths, arcs


# Function that takes as input the two dictionnaries (evac_paths + arcs) and prints them
def print_input_data(evac_paths, arcs):
    print("========================")
    print("INFORMATION D'EVACUATION")
    print("========================")
    print("Nombre de noeuds à évacuer : " + str(len(evac_paths)))
    print("----------")
    for keys, values in evac_paths.items():
        print(keys)
        print(values)

    print("")
    print("==============")
    print("ARCS DU GRAPHE")
    print("==============")
    print("Nombre d'arcs : " + str(len(arcs)))
    print("-----------------")
    for keys, values in arcs.items():
        print(keys)
        print(values)


# Parses solution data
def parse_solution(path):

    solution = {}  # {'instance_name', 'nb_evac_nodes', 'node_data', 'validity', 'aim_function', 'time', 'method'}

    myfile = open(path, 'r')
    l = myfile.readline()
    solution['instance_name'] = l.rstrip('\n')
    l = myfile.readline()
    solution['nb_evac_nodes'] = int(l)
    node_data = {}  # {'id', evac_rate, 'start'}

    for i in range(solution['nb_evac_nodes']):
        l = myfile.readline()
        ins = l.split()
        node_data[int(ins[0])] = (int(ins[1]), int(ins[2]))

    solution['node_data'] = node_data

    l = myfile.readline()
    solution['validity'] = l.rstrip('\n')
    l = myfile.readline()
    solution['aim_function'] = int(l)
    l = myfile.readline()
    solution['time'] = int(l)
    l = myfile.readline()
    solution['method'] = l.rstrip('\n')

    return solution


def __main__():
    evac_path, arc = parse_instance('./Exemple/graphe-TD-sans-DL-data.txt')
    print_input_data(evac_path, arc)
    sol = parse_solution('./Exemple/graphe-TD-sans-DL-sol.txt')
    print(sol)
