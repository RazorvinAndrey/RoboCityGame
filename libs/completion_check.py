import numpy as np
class DirectedHamiltonianCycle:
    def __init__(self, graph):
        self.graph = graph
        self.V = len(graph)
        self.cycles = []

    def is_safe(self, v, pos, path):
        if self.graph[path[pos - 1]][v] == 0:
            return False
        if v in path:
            return False
        return True

    def ham_cycle_util(self, path, pos):
        if pos == self.V:
            if self.graph[path[pos - 1]][path[0]] == 1:
                # Сохраняем найденный цикл
                self.cycles.append(path + [path[0]])  # Добавляем возврат к началу
            return

        for v in range(self.V):
            if self.is_safe(v, pos, path):
                path[pos] = v
                self.ham_cycle_util(path, pos + 1)
                path[pos] = -1  # Возврат (backtrack)

    def ham_cycle(self, start_node=0):
        path = [-1] * self.V
        path[0] = start_node  # Начинаем с указанной вершины
        self.ham_cycle_util(path, 1)
        return self.cycles

def dict_graph_to_matrix(dict_graph):
    out_matrix = np.zeros((len(dict_graph), len(dict_graph)), dtype=int)
    for from_node, out_node in dict_graph.items():
        for i in range(len(out_node)):
            out_matrix[from_node-1, out_node[i]-1] = 1
    return out_matrix

def completion_test(dict_graph, start_pos):
    graph = dict_graph_to_matrix(dict_graph)
    hc = DirectedHamiltonianCycle(graph)
    cycles = hc.ham_cycle(start_pos - 1)
    if not cycles:
        return False
    else:
        return True
