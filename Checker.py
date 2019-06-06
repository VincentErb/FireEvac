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
    arcs = ir.reverse_arcs(arcs)

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
                    print("pb maxrate")
                    print(prev)
                    print(current_node)
                    print(evac_rate)

                # Update on previous node to advance in route
                prev = current_node
        else:
            valid = False
    return valid


# Creates gantt blocks from evac data, solution data, and arcs from input data
# To be used in capacity check
def create_gantt(solution, evac_paths, arcs):
    arcs = ir.reverse_arcs(arcs)
    gantt = {}                                                          # {'start_node', ('n1', 'n2'): 'evac_rate', 'start'}
    solution_nodes = solution['node_data']

    for node_id, values in evac_paths.items():
        prev = node_id
        (evac_rate, start) = solution_nodes[node_id]
        for current in values['route_nodes']:

            if prev < current:
                gantt[(node_id, (prev, current))] = (evac_rate, start)
                start = start + arcs[(prev, current)]['length']
            else:
                gantt[(node_id, (prev, current))] = (evac_rate, start)
                start = start + arcs[(current, prev)]['length']
            prev = current

        gantt[(node_id, (prev, 'done'))] = (evac_rate, start)

    # print(gantt)
    return gantt


def calculate_objective(evac_nodes, gantt):
    endlist = []
    for key in gantt:
        if key[1][1] == 'done':
            st = gantt[key][1]
            pop = evac_nodes[int(key[0])]['pop']
            rate = evac_nodes[int(key[0])]['max_rate']
            tmp = pop % rate
            if tmp == 0:
                endlist.append(st + pop // rate)
            else:
                endlist.append(st + (pop // rate) + 1)

    return max(endlist)


# Verifies capacity with gantt
def check_capacity(evac_nodes, arcs, gantt):
    arcs = ir.reverse_arcs(arcs)
    valid = True

    relevent_arcs = set()

    for key in gantt:
        if key[1][1] != 'done':
            relevent_arcs.add(key[1])

    for i in relevent_arcs:
        if i[0] < i[1]:
            cap = arcs[i]['capacity']
        else:
            cap = arcs[(i[1], i[0])]['capacity']

        info = []
        for k in gantt:
            if k[1] == i:
                if evac_nodes[k[0]]['pop'] % gantt[k][0] == 0:
                    info.append([gantt[k][0], gantt[k][1], evac_nodes[k[0]]['pop'] // gantt[k][0], gantt[k][0]])
                else:
                    info.append([gantt[k][0], gantt[k][1], (evac_nodes[k[0]]['pop'] // gantt[k][0]) + 1, evac_nodes[k[0]]['pop'] % gantt[k][0]])
        # print(cap)
        # print(info)

        start = min(info)[1]
        end = max([s+d for (c, s, d, l) in info])

        # print(start)
        # print(end)

        # For every time unit
        for j in range(start, end):
            current_pers = 0
            for (ra, st, ft, last) in info:
                if st <= j < st + ft - 1:
                    current_pers = current_pers + ra
                # GESTION DERNIER BLOC
                elif j == st + ft - 1:
                    current_pers = current_pers + last
            if current_pers > cap:
                print(i, "problem capacity =", cap)
                print(current_pers)
                valid = False

        return valid


def test():
    evac, ark = ir.parse_instance('./Exemple/graphe-TD-sans-DL-data.txt')
    sol = ir.parse_solution('./Exemple/graphe-TD-sans-DL-sol.txt')

    print(check_max_rate(sol, evac, ark))

    g = create_gantt(sol, evac, ark)
    # print(calculate_objective(evac, g))
    print(check_capacity(evac, ark, g))


def run(instance_path, solution_path):
    evac, ark = ir.parse_instance(instance_path)
    sol = ir.parse_solution(solution_path)
    print("Checking max rate ... ", end='')
    if check_max_rate(sol,evac,ark):
        print("OK")
    else:
        print("FAILED")
    print("Checking capacity ... ", end='')

    g = create_gantt(sol, evac, ark)
    if check_capacity(evac, ark, g):
        print("OK")
    else:
        print("FAILED")

    print("Objective function value : ", end='')
    print(calculate_objective(evac, g))


# RUN THIS FUNCTION WITH A SOLUTION DICO CONTAINING THE FIELD "node_data"
def run_dico(instance_path, solution_dico):
    evac, ark = ir.parse_instance(instance_path)
    sol = solution_dico
    print("Checking max rate ... ", end='')
    if check_max_rate(sol, evac, ark):
        print("OK")
    else:
        print("FAILED")
    print("Checking capacity ... ", end='')

    g = create_gantt(sol, evac, ark)
    if check_capacity(evac, ark, g):
        print("OK")
    else:
        print("FAILED")

    print("Objective function value : ", end='')
    print(calculate_objective(evac, g))


def run_with_objective(instance_path, solution_dico):
    valid = True
    evac, ark = ir.parse_instance(instance_path)
    sol = solution_dico
    # print("Checking max rate ... ", end='')
    if not(check_max_rate(sol, evac, ark)):
        print("Max_rate")
        valid = False

    # print("Checking capacity ... ", end='')
    g = create_gantt(sol, evac, ark)
    if not(check_capacity(evac, ark, g)):
        print("capacity")

        valid = False

    return valid, calculate_objective(evac, g)


def run_with_objective_parsed(evac, ark, solution_dico):
    valid = True
    sol = solution_dico
    # print("Checking max rate ... ", end='')
    if not(check_max_rate(sol, evac, ark)):
        print("Max_rate")
        valid = False

    # print("Checking capacity ... ", end='')
    g = create_gantt(sol, evac, ark)
    if not(check_capacity(evac, ark, g)):
        print("capacity")

        valid = False

    return valid, calculate_objective(evac, g)

# run('./Exemple/graphe-TD-sans-DL-data.txt', './Exemple/graphe-TD-sans-DL-sol.txt')
