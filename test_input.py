from libs import robositygame as rcg

graph, model, com_flag = rcg.init_game(1, 0, [[14, 7], [7, 14]])
if not com_flag:
    print("This track cannot be completed! Change base_info!")
# ЗДЕСЬ НАЧИНАЮТСЯ ВАШИ КОММАНДЫ/АЛГОРИТМ
model.mov_to_front_point()
model.mov_to_front_point()
model.mov_to_right_point()
#ЗДЕСЬ ЗАКАНЧИВАЮТСЯ ВАШИ КОМАНДЫ/АЛГОРИТМ
rcg.finalize(model=model, graph=graph)