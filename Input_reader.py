import numpy as np


# Object that describes the parameters of an arc (used in arc matrix)
class ArcParameters:
    def __init__(self, duedate, length, capacity):
        self.duedate = duedate
        self.length = length
        self.capacity = capacity


class InputData:
    def __init__(self):
        self.num_evac_nodes = None
        self.safe_node = None
        self.num_nodes = None
        self.num_arcs = None
        self.evac_info = None
        self.arcs = None

    def parsedata(self, path):
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
                self.num_evac_nodes = int(l[0])
                self.safe_node = int(l[1])
                self.evac_info = np.empty([int(self.num_evac_nodes), 5], dtype=object)

                for j in range(0, int(self.num_evac_nodes)):
                    i = i + 1
                    l = ins[i]
                    l = l.split(" ")
                    self.evac_info[j, 0] = int(l[0])                    # id of node
                    self.evac_info[j, 1] = int(l[1])                    # population
                    self.evac_info[j, 2] = int(l[2])                    # max rate
                    self.evac_info[j, 3] = int(l[3])                    # k : length of route
                    self.evac_info[j, 4] = np.empty([int(l[3])])     # escape route nodes

                    for k in range(0, int(l[3])):
                        self.evac_info[j, 4][k] = int(l[4 + k])

                i = i + 1
                state = 1

            elif state == 1:
                self.num_nodes = int(l[0])
                self.num_arcs = int(l[1])
                self.arcs = np.empty([int(self.num_nodes), self.num_nodes], dtype=object)

                for j in range(0, int(self.num_arcs)):
                    i = i + 1
                    l = ins[i]
                    l = l.split(" ")
                    tmp = ArcParameters(int(l[2]), float(l[3]), float(l[4]))
                    self.arcs[int(l[0]), int(l[1])] = tmp

                state = -1

            else:
                i = i + 1

    def print_input_data(self):

        print("========================")
        print("INFORMATION D'EVACUATION")
        print("========================")
        print("Nombre de noeuds à évacuer : " + str(self.num_evac_nodes))
        print("Sortie : " + str(self.safe_node))
        print("----------")
        for i in range(0, self.num_evac_nodes):
            s = "Trajet : " + str(self.evac_info[i][0])
            for j in range(0, self.evac_info[i][3]):
                s = s + " - " + str(self.evac_info[i][4][j])

            s = s + " || Population : " + str(self.evac_info[i][1]) + " || Taux d'évacuation max : " \
                + str(self.evac_info[i][2])
            print(s)

        print("")
        print("==============")
        print("ARCS DU GRAPHE")
        print("==============")
        print("Nombre de noeuds : " + str(self.num_nodes))
        print("Nombre d'arcs : " + str(self.num_arcs))
        print("-----------------")
        for i in range(0, self.num_nodes):
            for j in range(0, self.num_nodes):
                if self.arcs[i, j] is not None:
                    print("(" + str(i) + "," + str(j) + ") - Duedate : " + str(self.arcs[i, j].duedate)
                          + " || Length : " + str(self.arcs[i, j].length) + " || Capacity : "
                          + str(self.arcs[i, j].capacity))


test = InputData()
test.parsedata('./Exemple/graphe-TD-sans-DL-data.txt')
test.print_input_data()
