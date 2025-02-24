from libs import robositygame as rcg
from libs import robocitydisp as rcd

if __name__ == '__main__':
    graph, model, com_flag = rcg.init_game(1, (270 % 360), [], [10, 9, 7])
    if not com_flag:
        print("This track cannot be completed! Change base_info!")
    # ЗДЕСЬ НАЧИНАЮТСЯ ВАШИ КОММАНДЫ/АЛГОРИТМ
    #model.rotate(-90)
    model.go_forward()
    model.rotate(90)
    model.go_forward()
    model.rotate(-90)
    model.go_forward()
    model.rotate(-90)
    model.go_forward()
    #ЗДЕСЬ ЗАКАНЧИВАЮТСЯ ВАШИ КОМАНДЫ/АЛГОРИТМ
    rcg.finalize(model=model, graph=graph, mode='capture_flag')
    rcd.draw_result(model.recorder, graph.base_info)