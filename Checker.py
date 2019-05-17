import FireEvac.Input_reader as ir

# CHECKER
# Will run three checks for validity :
# First, it will check max_rate on all arcs of safe routes
# Then, it will represent the solution with Gant blocks to verify that capacity is respected


# Returns true if solution's max_rate respects max_rate of arcs on the path
# Returns false otherwise
def check_max_rate(solution, evac_paths, arcs):
    solution_nodes = solution['node_data']
    valid = True

    for node_id, values in evac_paths.items():
        # Solution evac_rate
        evac_rate = solution_nodes[node_id][0]

        # Main evac rate check
        if evac_rate <= evac_paths[node_id]['max_rate']:
            prev = node_id

            # Route rate check
            for current_node in values['route_nodes']:
                if ((prev < current_node) and (evac_rate > arcs[(prev, current_node)]['capacity']))\
                        or ((current_node < prev) and (evac_rate > arcs[(current_node, prev)]['capacity'])):
                    valid = False

                # Update on previous node to advance in route
                prev = current_node
        else:
            valid = False
    return valid


# Creates gantt blocks from evac data, solution data, and arcs from input data
# To be used in capacity check
def create_gantt(solution, evac_paths, arcs):
    gantt = {}                                       # {'start_node', ('n1', 'n2'): 'evac_rate', 'start', 'end', 'tail'}
    solution_nodes = solution['node_data']

    for node_id, values in evac_paths.items():
        prev = node_id
        (evac_rate, start) = solution_nodes[node_id]
        end = 0
        for current in values['route_nodes']:

            if prev < current:
                end = start + (values['pop'] // arcs[(prev, current)]['capacity'])
                gantt[(node_id, (prev, current))] = (evac_rate, start, end)
                start = start + arcs[(prev, current)]['length']

            else:
                end = start + (values['pop'] // arcs[(current, prev)]['capacity'])
                gantt[(node_id, (prev, current))] = (evac_rate, start, end)
                start = start + arcs[(current, prev)]['length']

            prev = current

        end = -1
        gantt[(node_id, (prev, 'done'))] = (evac_rate, start, end)

    print(gantt)
    return gantt


# Verifies capacity with gantt
def check_capacity():
    print("coucou")


evac, ark = ir.parse_instance('./Exemple/graphe-TD-sans-DL-data.txt')
sol = ir.parse_solution('./Exemple/graphe-TD-sans-DL-sol.txt')

print(check_max_rate(sol, evac, ark))

create_gantt(sol, evac, ark)
