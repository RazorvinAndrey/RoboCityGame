import heapq
import itertools

def find_path(graph, weights, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]  # (расстояние, узел)
    previous_nodes = {node: None for node in graph}  # Для отслеживания пути

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break  # Найден конечный узел, можно завершить цикл

        if current_distance > distances[current_node]:
            continue

        # Рассматриваем соседние узлы и их веса
        neighbors = graph[current_node]
        neighbor_weights = weights[current_node]

        for neighbor, weight in zip(neighbors, neighbor_weights):
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node  # Сохраняем предшествующий узел
                heapq.heappush(priority_queue, (distance, neighbor))

    # Восстановление пути
    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path.reverse()  # Разворачиваем путь, чтобы он был в правильном порядке

    return distances[end], path  # Возвращаем кратчайшее расстояние и путь

def find_shortest_path(graph, weights, start, targets, come_back):
    min_distance = float('inf')
    best_path = []

    # Перебираем все перестановки целевых узлов
    for perm in itertools.permutations(targets):
        current_distance = 0
        current_node = start

        # Рассчитываем расстояние для текущей перестановки
        for target in perm:
            distance, path = find_path(graph, weights, current_node, target)
            if distance == float('inf'):
                current_distance = float('inf')
                break
            current_distance += distance
            current_node = target

        # Проверьте, является ли текущий путь кратчайшим
        if current_distance < min_distance:
            min_distance = current_distance
            best_path = [start] + list(perm)

    if come_back:
        distance, path = find_path(graph, weights, best_path[-1], start)
        print(best_path)
        min_distance += distance
        best_path = best_path + path

    return min_distance, best_path

if __name__ == '__main__':
    # Данные графа и весов
    GraphDict = {
        1: [2, 10],
        2: [1, 3, 12],
        3: [2, 4],
        4: [3, 5, 11],
        5: [4, 6, 14],
        6: [5, 7],
        7: [6, 8, 14],
        8: [7, 9, 15],
        9: [8, 10],
        10: [1, 9, 15],
        11: [12],
        12: [2, 13],
        13: [11, 15],
        14: [5, 7, 15],
        15: [8, 10, 13, 14]
    }

    WeightDict = {
        1: [5.5, 5.0],
        2: [5.5, 1.3, 2.5],
        3: [1.3, 3.0],
        4: [3.0, 1.0, 2.5],
        5: [1.0, 3.5, 2.4],
        6: [3.5, 2.4],
        7: [2.4, 2.4, 3.5],
        8: [2.4, 2.0, 2.5],
        9: [2.0, 2.5],
        10: [5.0, 2.5, 2.0],
        11: [0.5],
        12: [2.5, 1.0],
        13: [2.0, 2.5],
        14: [2.4, 3.5, 2.3],
        15: [2.5, 2.0, 2.5, 2.3]
    }
    # Пример использования
    # Данные графа
    start_node = 13
    target_nodes = [2, 3, 5, 15]
    return_to_sender = True
    shortest_path_distance, shortest_path = find_shortest_path(GraphDict, WeightDict, start_node, target_nodes, return_to_sender)

    if return_to_sender:
        print(f"Кратчайшее расстояние от узла {start_node} с посещением узлов {target_nodes} с возвратом: {shortest_path_distance}")
    else:
        print(
            f"Кратчайшее расстояние от узла {start_node} с посещением узлов {target_nodes} без возврата: {shortest_path_distance}")
    print(f"Путь: {' -> '.join(map(str, shortest_path))}")