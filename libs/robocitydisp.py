import pygame
node_pos_dict = {
    1 : (640,713),
    2 : (155,713),
    3 : (25,713),
    4 : (25,465),
    5 : (25,345),
    6 : (25,25),
    7 : (265,25),
    8 : (465,25),
    9 : (640,25),
    10 : (640,243),
    11 : (260,545),
    12 : (340,580),
    13 : (410,460),
    14 : (265,345),
    15 : (480,243)
}

pygame.init()
pygame.font.init()
rsg_font = pygame.font.SysFont('Comic Sans MS', 20)
window = pygame.display.set_mode((660, 740))
clock = pygame.time.Clock()
map = pygame.image.load("libs/new_city.png")
bibika = pygame.image.load("libs/bibika.png")
block = pygame.image.load("libs/blockade.png")
orig_bibika = bibika
orig_block = block
block_list = []

def map_draw(window, block_list):
    window.fill((255, 255, 255))
    window.blit(map, (0, 0))
    for i in range(1, 16):
        pygame.draw.circle(window, (0, 225, 0), node_pos_dict[i], 10)
        text = rsg_font.render(f'{i}', False, (0, 0, 0))
        window.blit(text, node_pos_dict[i])
    if len(block_list) != 0:
        for block in block_list:
            bck_node_1 = node_pos_dict[int(block[0])]
            bck_node_2 = node_pos_dict[int(block[1])]
            if (block[0] == 4 and block[1] == 11) or (block[1] == 4 and block[0] == 11):
                block_pose = (170, 520)
                if block[2] == 180:
                    block_rot = 325
                else:
                    block_rot = -325
            elif (block[0] == 13 and block[1] == 15) or (block[1] == 15 and block[0] == 13):
                block_pose = (480, 350)
                if block[2] == 180: block_rot = 270
                else: block_rot = 90
            elif (block[0] == 8 and block[1] == 15) or (block[1] == 15 and block[0] == 8):
                block_pose = ((int((bck_node_1[0]+bck_node_2[0])/2))-15, int((bck_node_1[1]+bck_node_2[1])/2))
                block_rot = int(block[2])
            else:
                block_pose = (int((bck_node_1[0]+bck_node_2[0])/2), int((bck_node_1[1]+bck_node_2[1])/2))
                block_rot = int(block[2])
            rect = orig_block.get_rect(center=block_pose)
            block_img, block_rect = rotate_img(orig_block, rect, block_rot)
            window.blit(block_img, block_rect)

def rotate_img(image, rect, angle):
    """Rotate the image while keeping its center."""
    # Rotate the original image without modifying it.
    new_image = pygame.transform.rotate(image, angle)
    # Get a new rect with the center of the old rect.
    rect = new_image.get_rect(center=rect.center)
    return new_image, rect

def mov_rot_img(window, image, new_pos, new_angle):
    rect = image.get_rect(center=(new_pos[0], new_pos[1]))
    image, rect = rotate_img(orig_bibika, rect, new_angle)
    map_draw(window, block_list)
    window.blit(image, rect)

def command_parse(logs):
    comms = []
    for log in logs:
        comms.append(log.split(" "))
    return comms

def base_info_parse(base_info):
    base_data = command_parse(base_info)
    for row in base_data:
        if row[0] == 'start':
            start_pos = int(row[1])
            start_rot = int(row[2])
        if row[0] == 'block':
            block_list.append([int(row[1]), int(row[2]), int(row[3])])
    return start_pos, start_rot

def draw_result(logs, base_info):
    start_pos, start_rot = base_info_parse(base_info)
    j = 0
    animation_start = False
    is_started = False
    is_finished = False
    i = 0
    cur_pos = start_pos
    cur_angle = start_rot
    mov_rot_img(window=window, image=orig_bibika, new_pos=node_pos_dict[cur_pos], new_angle=cur_angle)
    pygame.display.flip()
    comms = command_parse(logs)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_SPACE:
                    animation_start = True
        if animation_start:
            if not is_started:
                print("animation_start")
                is_started = True
            if j%60==0:
                if i < len(comms) and not is_finished:
                    if comms[i][0] == 'mov':
                        if comms[i][3] == 'succ':
                            cur_pos = int(comms[i][1])
                            cur_angle = int(comms[i][2])
                        elif comms[i][3] == 'fail' or comms[i][3] == 'erro':
                            print("ROAD COLLISION!")
                            is_finished = True
                    if comms[i][0] == 'rot':
                        cur_angle = int(comms[i][2])
                    i+=1
                else:
                    if not is_finished:
                        print("animation_finished")
                        is_finished = True
            mov_rot_img(window=window, image=orig_bibika, new_pos=node_pos_dict[cur_pos], new_angle=cur_angle)
            j+=1
            pygame.display.flip()
            clock.tick(60)
