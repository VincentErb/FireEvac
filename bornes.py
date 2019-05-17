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


evac, ark = ir.parse_instance('./Exemple/graphe-TD-sans-DL-data.txt')
# print(borne_inf(evac, ark))
# print(borne_sup(evac, ark))


