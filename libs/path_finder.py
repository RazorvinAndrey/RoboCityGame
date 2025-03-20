import heapq
import itertools
from copy import deepcopy

def find_path_with_rot(graph, weights, rots, start, end, start_rot, can_turn):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    rotation = start_rot
    priority_queue = [(0, start)]  # (расстояние, узел)
    previous_nodes = {node: None for node in graph}  # Для отслеживания пути
    firstNode = not can_turn
    rot_cand = None

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break  # Найден конечный узел, можно завершить цикл

        if current_distance > distances[current_node]:
            continue

        # Рассматриваем соседние узлы и их веса
        neighbors = graph[current_node]
        neighbor_weights = weights[current_node]
        neighbor_rots = rots[current_node]

        for neighbor, weight, rot in zip(neighbors, neighbor_weights, neighbor_rots):
            if firstNode and (rot != rotation):
                continue
            turn_angle = (rot - rotation) % 360
            if turn_angle > 180:
                turn_angle -= 360
            if abs(turn_angle) > 150:
                continue

            if current_node == 10 and end == 8:
                distance = current_distance + 2.5
                distances[9] = distance
                rot_cand = rot
                previous_nodes[9] = current_node
                heapq.heappush(priority_queue, (distance, 9))
                break

            if current_node == 5 and end == 7:
                distance = current_distance + 3.4
                distances[6] = distance
                rot_cand = rot
                previous_nodes[6] = current_node
                heapq.heappush(priority_queue, (distance, 6))
                break

            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                rot_cand = rot
                previous_nodes[neighbor] = current_node  # Сохраняем предшествующий узел
                heapq.heappush(priority_queue, (distance, neighbor))
        rotation = rot_cand
        if firstNode:
            firstNode = False


    # Восстановление пути
    print(previous_nodes)
    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path.reverse()  # Разворачиваем путь, чтобы он был в правильном порядке

    return distances[end], path, rotation  # Возвращаем кратчайшее расстояние и путь

def find_path_without_rot(graph, weights, start, end, prev_node):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]  # (расстояние, узел)
    previous_nodes = {node: None for node in graph}  # Для отслеживания пути
    past_node = prev_node

    while priority_queue:
        copy_graph = deepcopy(graph)
        copy_weights = deepcopy(weights)
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break  # Найден конечный узел, можно завершить цикл

        if current_distance > distances[current_node]:
            continue

        if past_node is not None and past_node in copy_graph[current_node]:
            idx = copy_graph[current_node].index(past_node)
            copy_graph[current_node].pop(idx)
            copy_weights[current_node].pop(idx)

        # Рассматриваем соседние узлы и их веса
        neighbors = copy_graph[current_node]
        neighbor_weights = copy_weights[current_node]

        for neighbor, weight in zip(neighbors, neighbor_weights):
            if neighbor == past_node:
                continue

            if current_node == 10 and end == 8:
                distance = current_distance + 2.5
                distances[9] = distance
                previous_nodes[9] = current_node
                heapq.heappush(priority_queue, (distance, 9))
                break

            if current_node == 5 and end == 7:
                distance = current_distance + 3.4
                distances[6] = distance
                previous_nodes[6] = current_node
                heapq.heappush(priority_queue, (distance, 6))
                break

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
    print(path)

    return distances[end], path  # Возвращаем кратчайшее расстояние и путь

def find_shortest_path(graph, weights, rots, start, start_rot, targets):
    min_distance = float('inf')
    best_path = []
    if start in targets:
        targets.remove(start)

    # Перебираем все перестановки целевых узлов
    for perm in itertools.permutations(targets):
        rotat = start_rot
        current_distance = 0
        current_node = start
        turning = False
        paths = [start]

        # Рассчитываем расстояние для текущей перестановки
        for target in perm:
            if target in paths:
                continue
            if not turning:
                distance, path, cur_rot = find_path_with_rot(graph, weights, rots, current_node, target, rotat, turning)
            else:
                distance, path  = find_path_without_rot(graph, weights, current_node, target, paths[-2])
            if distance == float('inf'):
                current_distance = float('inf')
                break
            current_distance += distance
            current_node = target
            paths += path[1:]
            rotat = cur_rot
            turning = True
            if set(targets).issubset(paths):
                break
        print(f'list {list(perm)}')
        print(f'dist {current_distance}')

        # Проверьте, является ли текущий путь кратчайшим
        if current_distance < min_distance:
            min_distance = current_distance
            best_path = paths
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
        11: [4, 12],
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
        9: [5.0, 2.0, 2.5],
        10: [5.0, 2.5, 2.0],
        11: [2.5, 0.5],
        12: [2.5, 1.0],
        13: [2.0, 2.5],
        14: [2.4, 3.5, 2.3],
        15: [2.5, 2.0, 2.5, 2.3]
    }
    RotDict = {
        1: [0, 270],
        2: [180, 0, 270],
        3: [180, 270],
        4: [90, 270, 180],
        5: [90, 270, 180],
        6: [90, 180],
        7: [0, 180, 90],
        8: [0, 180, 90],
        9: [0, 90],
        10: [90, 270, 0],
        11: [0, 90],
        12: [90, 180],
        13: [270, 180],
        14: [0, 270, 180],
        15: [270, 180, 90, 0]
    }
    # Пример использования
    # Данные графа
    start_node = 1
    start_rot = 270
    target_nodes = [1, 5, 7, 10]
    dist, path, rot = find_path_with_rot(GraphDict, WeightDict, RotDict, 1, 10, 270, False)
    print(f'distance {dist}')
    print(f'path chosen {path}')
    dist, path = find_path_without_rot(GraphDict, WeightDict, 10, 5, 1)
    print(f'distance {dist}')
    print(f'path chosen {path}')
    dist, path = find_path_without_rot(GraphDict, WeightDict, 5, 7, 8)
    print(f'distance {dist}')
    print(f'path chosen {path}')
    shortest_path_distance, shortest_path = find_shortest_path(GraphDict, WeightDict, RotDict, start_node, start_rot, target_nodes)
    print(f"Кратчайшее расстояние от узла {start_node} с посещением узлов {target_nodes} без возврата: {shortest_path_distance}")
    print(f"Путь: {' -> '.join(map(str, shortest_path))}")