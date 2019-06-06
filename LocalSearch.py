import FireEvac.Input_reader as ir
import FireEvac.Checker as chk
import FireEvac.Bornes as brn
from copy import deepcopy
import random as rd


def local_search(evac_path, arcs, solution):
    nb_accept = 50
    cpt_validity = 0 # goes from 0 to nb_accept to allow non-valid solution for a time
    ite = 5000
    modif_true = [solution, 100000, True]
    modif_false = [solution, 100000, False]
    better_solution = solution
    list_start_node = []
    for keys, values in evac_path.items():
        list_start_node.append(keys)
    while ite > 0:
        ite = ite - 1
        if modif_true[1] == brn.borne_inf(evac_path, arcs):
            break
        else:
            for i in range(20):
                a = rd.randint(0, len(list_start_node)-1)
                b = rd.randint(0, 3)
                v, check_better_solution = chk.run_with_objective_parsed(evac_path, arcs, better_solution)
                new_solution = modify_solution(better_solution, list_start_node[a], b)  # we modify one paramater of one path
                valid, check_new_solution = chk.run_with_objective_parsed(evac_path, arcs, new_solution)
                #print("new", chk.run_with_objective_parsed(evac_path, arcs, new_solution))
                #print("better", chk.run_with_objective_parsed(evac_path, arcs, better_solution))
                if check_better_solution >= check_new_solution:
                    if valid:
                        cpt_validity = 0
                        better_solution = new_solution
                        modif_true[0] = better_solution
                        modif_true[1] = check_new_solution
                    else:
                        if cpt_validity < nb_accept:
                            better_solution = new_solution
                            cpt_validity = cpt_validity + 1
                            modif_false[0] = better_solution
                            modif_false[1] = check_new_solution
                        else:
                            better_solution = modif_true[0]
    print(modif_true)

    return new_solution


def modify_solution(solution, path_to_modify, modification):
    # modification : 0 -> -1 on evac_rate, 1 -> +1 on evac_rate, 2 -> -1 on start 3-> +1 on start
    # print(solution['node_data'])
    sol = deepcopy(solution)
    a, b = sol['node_data'][path_to_modify]
    if modification == 0:
        if a != 1:
            (a, b) = (a - 1, b)
    elif modification == 1:
        (a, b) = (a + 1, b)
    elif modification == 2:
        if b != 0:
            (a, b) = (a, b - 1)
    elif modification == 3:
        (a, b) = (a, b + 1)
    sol['node_data'][path_to_modify] = (a, b)
    return sol



evac, ark = ir.parse_instance('./Instances/sparse_10_30_3_7_I.full')
#print(chk.run_with_objective('./Instances/sparse_10_30_3_2_I.full',brn.borne_sup_solution(evac, ark) ))
local_search(evac, ark, brn.borne_sup_solution(evac, ark))


#evac, ark = ir.parse_instance('./Exemple/graphe-TD-sans-DL-data.txt')
#local_search(evac, ark,  brn.borne_sup_solution(evac, ark))

