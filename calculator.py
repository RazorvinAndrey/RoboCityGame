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