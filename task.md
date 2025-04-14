входные параметры:
gen_line  (строка с маршрутом тачки, по типу "1-2-3-4-...")
start_pos - стартовая позиция
start_rot - стартовый курс
blocks -информация о заблокированных путях
flags - информация о том, какие точки следует посетить

на выходе: 
выход функции rcg.finalize_to_vizual_interface(gen_graph, gen_rover)


функция (нужно будет её поменять так, чтобы она не выводила принты, а возвращала значения, которые ты будешь использовать в интерфейсе):
def finalize_to_vizual_interface(graph, model): # mode='capture_flag'
    res = set(graph.flag_pos) & set(model.has_flag)
    if model.distance <= 0:
        print('Rover didn\'t move at all!')
        print('SCORE - 0%')
        return
    elif len(res) == len(graph.flag_pos):
        print('All flags have ёbeen captured!')
    else:
        print('Some spots where missed')
    optima, _ = pf.find_shortest_path(graph.GraphDict, graph.WeightDict, graph.RotDict, model.start_pos, model.start_rot, list(res))
    length = (optima / model.distance) * (len(res) / len(graph.flag_pos))
    print(f'SCORE - {round(length * 100, 3)}%')

основной код:
from libs import robositygame as rcg

gen_line = '1-2-3-4-11'
start_pos = 1
start_rot = 0
blocks = []
flags = [12, 3]

gen_graph, gen_rover, com_flag = rcg.init_game(start_pos, start_rot, blocks, flags)

def line_parces(line):
    path = []
    path_str = line.split("-")
    if len(path_str) < 1:
        print("something went wrong")
        return None
    for point in path_str:
        if int(point) > 15 or int(point) < 1:
            print("inputed data is flawed")
            return None
        path.append(int(point))
    return path

def find_length(path, rover):
    for i in range(1, len(path)):
        if not rover.mov_to_point(path[i]):
            print("something went wrong!")
            return None
    return rover.distance

if __name__ == '__main__':
    path = line_parces(gen_line)
    find_length(path, gen_rover)
    rcg.finalize(gen_graph, gen_rover)
    rcg.finalize_to_vizual_interface(gen_graph, gen_rover)

задача: написать визуальный интерфейс (отдельным файлом, который я буду запускать) для ввода и вывода. дизайн aperture science. слева должна быть картинка (libs/new city.png), которую можно будет скрыть. 