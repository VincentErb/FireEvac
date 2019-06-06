import FireEvac.Input_reader as ir


# Maximum of the length of each evacuation, every evacuation proceeds as if i was the only one
def borne_inf(evac_path, arcs):
    inf = 0
    for keys, values in evac_path.items():
        long_route = 0
        prev = keys

        # Length of a path
        for current_node in values['route_nodes']:
            if prev < current_node:
                long_route = long_route + arcs[(prev, current_node)]['length']

            else:
                long_route = long_route + arcs[(current_node, prev)]['length']
            # Update on previous node to advance in route
            prev = current_node

        if values['pop'] % values['max_rate'] == 0:
            trip = long_route + values['pop'] // values['max_rate']
        else:
            trip = long_route + values['pop'] // values['max_rate'] + 1
        if trip > inf:
            inf = trip
    return inf


# Sum of the length of consecutive evacuations, the N-th evacuation start after the end of N-1-th evacuation
def borne_sup(evac_path, arcs):
    sup = 0
    for keys, values in evac_path.items():
        long_route = 0
        prev = keys

        # Length of a path
        for current_node in values['route_nodes']:
            if prev < current_node:
                long_route = long_route + arcs[(prev, current_node)]['length']

            else:
                long_route = long_route + arcs[(current_node, prev)]['length']
            # Update on previous node to advance in route
            prev = current_node

        if values['pop'] % values['max_rate'] == 0:
            trip = long_route + values['pop'] // values['max_rate']
        else:
            trip = long_route + values['pop'] // values['max_rate'] + 1
        sup = sup + trip
    return sup


def borne_sup_solution(evac_path, arcs):
    solution = {}  # {'instance_name', 'nb_evac_nodes', 'node_data', 'validity', 'aim_function', 'time', 'method'}
    solution['instance_name'] = "Sup-borne-solution"
    solution['nb_evac_nodes'] = len(evac_path)
    start = 0

    node_data = {}  # {'id', evac_rate, 'start'}
    for keys, values in evac_path.items():
        long_route = 0
        prev = keys

        # Length of a path
        for current_node in values['route_nodes']:
            if prev < current_node:
                long_route = long_route + arcs[(prev, current_node)]['length']

            else:
                long_route = long_route + arcs[(current_node, prev)]['length']
            # Update on previous node to advance in route
            prev = current_node

        if values['pop'] % values['max_rate'] == 0:
            trip = long_route + values['pop'] // values['max_rate']
        else:
            trip = long_route + values['pop'] // values['max_rate'] + 1
        node_data[keys] = (values['max_rate'], start)
        print(values['max_rate'])
        start = start + trip # make the next evacuation node begin after the previous one as finished evacuating
    solution['node_data'] = node_data

    solution['validity'] = "valid"
    solution['aim_function'] = borne_inf(evac_path,arcs)
    solution['time'] = borne_sup(evac_path,arcs)
    solution['method'] = "consecutive-evacuation"
    return solution

evac, ark = ir.parse_instance('./Exemple/graphe-TD-sans-DL-data.txt')
# print(borne_inf(evac, ark))
print(borne_sup(evac, ark))


