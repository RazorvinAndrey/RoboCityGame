from libs import robositygame as rcg

graph, model, com_flag = rcg.init_game(1, 0, [[4, 5], [8, 15]])
if com_flag:
    # ЗДЕСЬ НАЧИНАЮТСЯ ВАШИ КОММАНДЫ/АЛГОРИТМ
    model.mov_to_front_point()
    model.mov_to_front_point()
    model.mov_to_right_point()
    model.mov_to_right_point()
    model.mov_to_front_point()
    model.mov_to_front_point()
    model.mov_to_right_point()
    model.mov_to_left_point()
    model.mov_to_front_point()
    model.mov_to_right_point()
    model.mov_to_right_point()
    model.mov_to_front_point()
    model.mov_to_front_point()
    model.mov_to_right_point()
    model.mov_to_front_point()
    #ЗДЕСЬ ЗАКАНЧИВАЮТСЯ ВАШИ КОМАНДЫ/АЛГОРИТМ
else:
    print("This track cannot be completed! Change base_info!")
rcg.finalize(model=model, graph=graph)