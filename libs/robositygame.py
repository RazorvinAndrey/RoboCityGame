from libs import completion_check as cc, path_finder as pf

game_modes = ['roundabout', 'flag_capture']

class Graph:
    def __init__(self):
        self.GraphDict = {
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
        self.WeightDict = {
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
        self.RotDict = {
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
            11: [90],
            12: [90, 180],
            13: [270, 180],
            14: [0, 270, 180],
            15: [270, 180, 90, 0]
        }
        self.base_info = []
        self.flag_pos = []

    def put_obstacle(self, nodes):
        if nodes[1] in self.GraphDict[nodes[0]]:
            del_index = self.GraphDict[nodes[0]].index(nodes[1])
            self.GraphDict[nodes[0]].pop(del_index)
            self.WeightDict[nodes[0]].pop(del_index)
            rot_block = self.RotDict[nodes[0]].pop(del_index)
            print(f"Path from {nodes[0]} to {nodes[1]} is blocked!")
            self.base_info.append(f"block {nodes[0]} {nodes[1]} {rot_block}")
        else:
            print("Cannot remove smth that doesn't exist")

    def put_flag(self, pos):
        if 0 < pos < 16:
            self.flag_pos.append(pos)
            print(f'Flag added on position {pos}')
            self.base_info.append(f"flag {pos}")
        else:
            print('Cannot put Flag there!')


class Rover:
    def __init__(self, cur_pos, cur_rot, graph):
        self.start_pos = cur_pos
        self.pos = cur_pos
        if cur_pos > 0 and cur_pos < 16:
            self.star_rot = cur_rot
        else:
            print("Cannot initialize here. Assuming starting position at point 1")
            self.star_rot = 1
        self.prev_pos = None
        self.cur_rot = cur_rot % 360
        self.graph = graph
        self.distance = 0
        self.route = [self.pos]
        self.has_flag = []
        self.moved_before = False
        if len(self.graph.flag_pos) > 0:
            if self.pos in self.graph.flag_pos:
                self.has_flag.append(self.pos)
        self.recorder = []
        graph.base_info.append(f"start {cur_pos} {cur_rot}")

    def mov_to_point(self, point):
        if point > 0 and point < 16:
            if point in self.graph.GraphDict[self.pos]:
                dest_index = self.graph.GraphDict[self.pos].index(point)
                if point == 11:
                    self.cur_rot = 90
                elif point == 12:
                    self.cur_rot = 180
                elif point == 13 and self.pos == 12:
                    self.cur_rot = 270
                elif point == 13 and self.pos == 15:
                    self.cur_rot = 0
                elif point == 15 and self.pos == 13:
                    self.cur_rot = 270
                self.route.append(point)
                self.prev_pos = self.pos
                self.pos = point
                self.distance += self.graph.WeightDict[self.prev_pos][dest_index]
                print(f"Rover has moved from node {self.prev_pos} to node {self.pos}")
                print(f"Current rot is {self.cur_rot} degrees")
                print(f"Distance went - {self.graph.WeightDict[self.prev_pos][dest_index]} m, Total - {self.distance} m")
                if not self.pos in self.has_flag and len(self.graph.flag_pos) > 0:
                    if self.pos in self.graph.flag_pos:
                        self.has_flag.append(self.pos)
                        print('Flag Captured!')
                self.recorder.append(f"mov {self.pos} {self.cur_rot} succ")
            else:
                print("Node not connected to the current position!")
                self.recorder.append(f"mov {self.pos} fail")
        else:
            print("There is no such node!")
            self.recorder.append(f"mov {self.prev_pos} {self.pos} erro")

    def rotate(self, degrees):
        if not self.moved_before:
            print('Can\'t rotate without prior movement!')
            self.recorder.append(f"rot {degrees} {self.cur_rot} fail")
            return
        if degrees < -135:
            degrees = -135
        elif degrees > 135:
            degrees = 135
        self.cur_rot = (self.cur_rot + degrees) % 360
        print(f"New Course - {self.cur_rot} degrees")
        self.moved_before = False
        self.recorder.append(f"rot {degrees} {self.cur_rot} succ")

    def go_forward(self):
        course = self.cur_rot
        if course in self.graph.RotDict[self.pos]:
            point = self.graph.GraphDict[self.pos][self.graph.RotDict[self.pos].index(course)]
            self.mov_to_point(point)
            self.moved_before = True
        else:
            print("Going off course!")
            self.recorder.append(f"mov {self.prev_pos} {self.pos} fail")

def finalize(mode, graph, model):
    if mode == 'roundabout':
        has_returned = False
        been_everywhere = False
        rout_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        left_meter = 0
        if model.route[0] == model.route[-1]:
            has_returned = True
            print("Car returned to start position")
        else:
            print("Car didn't returned to start position")
        for i in range(15):
            if rout_array[i] not in model.route[1:]:
                print(f"Car didn't visit point {rout_array[i]}")
                left_meter+=1
        if left_meter == 0:
            been_everywhere = True
            print("Car visited all points")
        else:
            print("Car missed some points")
        if been_everywhere and has_returned:
            commi_coeff = 38.8/model.distance
            score = round(float(30.0 * commi_coeff), 3)
        else:
            score = round(float(15.0/14.0 * (15.0-left_meter)), 3)
        print(f"SCORE - {score} points")
        #rcd.draw_result(model.recorder, graph.base_info)
    elif mode == 'capture_flag':
        res = set(graph.flag_pos) & set(model.has_flag)
        if model.distance <= 0:
            print('Rover didn\'t move at all!')
            print('SCORE - 0%')
            return
        elif len(res) == len(graph.flag_pos):
            print('All flags have been captured!')
        else:
            print('Some spots where missed')
        optima, _ = pf.find_shortest_path(graph.GraphDict, graph.WeightDict, model.start_pos, list(res), False)
        length = (optima / model.distance) * (len(res) / len(graph.flag_pos))
        print(f'SCORE - {round(length * 100, 3)}%')

def init_game(start_pos, start_rot, blocks=[], flags=[10, 11]):
    graph = Graph()
    if len(blocks) > 0:
        for block in blocks:
            graph.put_obstacle(block)
    if len(flags) > 0:
        for flag in flags:
            graph.put_flag(flag)
    can_be_completed = cc.completion_test(graph.GraphDict, 1)
    model = Rover(start_pos, start_rot, graph)
    return graph, model, can_be_completed

if __name__ == '__main__':
    graph, rover, comp = init_game(1, 0, [(1, 10)])
    dist, path = pf.round_trip(graph,1, 10)
    print(dist, path)
