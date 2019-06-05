import FireEvac.Input_reader as ir
import FireEvac.Checker as chk
import random as rd

def local_search(solution):
    nb_accept = 5
    cpt_validity = 0 # goes from 0 to nb_accept to allow non-valid solution for a time
    value = 10000
    ite = 1000
    while ite > 0 :
        ite = ite -1
        modif_table = {}
        better_solution = solution
        for i in range(10):
            a = rd.randint(0,solution['nb_evac_nodes']+1)
            b = rd.randint(0,4)
            new_solution = modify_solution(solution, a, b) # we modify one paramater of one path
            if check_better_solution > check_new_solution() :
                if valid:
                    cpt_validity = 0
                    better_solution = new_solution
                else:
                    if cpt_validity < nb_accept :
                        better_solution = new_solution
                        cpt_validity = cpt_validity + 1



        modif_table[ite]= { 'solution' : better_solution,'result' : result, 'validity' : validity}
        solution = better_solution

    for keys, values in modif_table.items() :
        if value > values['result'] and values['validity'] == 0:
            new_solution = values['solution']
            value = values['result']


    return new_solution

def modify_solution(solution, path_to_modify, modification):
    # modification : 0 -> -1 on evac_rate, 1 -> +1 on evac_rate, 2 -> -1 on start 3-> +1 on start
    i = 0
    for values in solution.items():
        if i == path_to_modify :
            (a, b) = values['node_data']
            if modification == 0:
                if a != 0 :
                    (a, b) = (a - 1, b)
            elif modification == 1:
                (a, b) = (a + 1, b)
            elif modification == 2:
                if b != 0 :
                    (a,b) = (a, b - 1)
            elif modification == 3:
                (a, b) = (a, b + 1)
            values['node_data'] = (a, b)
        i = i + 1
    return solution