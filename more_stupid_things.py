import networkx as nx
import itertools

G = nx.Graph()
G.add_edge(1, 2, weight=4)
G.add_edge(1, 3, weight=2)
G.add_edge(2, 4, weight=3)
G.add_edge(3, 4, weight=1)
G.add_edge(4, 5, weight=2)

nodes_to_visit = [2, 3, 4]

permutations = itertools.permutations(nodes_to_visit)

start_node = 1
end_node = 5
shortest_path = None
min_length = float('inf')

shortest_path = nx.shortest_path(G, source=1, target=5, weight='weight')
print(shortest_path)

for perm in permutations:
    current_path = [start_node] + list(perm) + [end_node]
    path_length = sum(G[u][v]['weight'] for u, v in zip(current_path[:-1], current_path[1:]))

    if path_length < min_length:
        min_length = path_length
        shortest_path = current_path

print("Кратчайший путь с посещением узлов:", shortest_path)
print("Длина пути:", min_length)

