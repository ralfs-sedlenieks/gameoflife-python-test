import argparse
import numpy
import os
import sys
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "no"

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PAUSED = False


def process_key_event(key):
    if key == pygame.K_RETURN or key == pygame.K_ESCAPE:
        quit_event = pygame.event.Event(pygame.QUIT)
        pygame.event.post(quit_event)
    elif key == pygame.K_SPACE:
        global PAUSED
        PAUSED = not PAUSED


def process_mouse_event(pos):
    matrix_pos = tuple(x//multiplier for x in pos)
    random_matrix[matrix_pos] = not random_matrix[matrix_pos]
    square.fill(BLACK if random_matrix[matrix_pos] == 0 else WHITE)
    cur_px = pygame.Rect(matrix_pos[0]*multiplier, matrix_pos[1]*multiplier, multiplier, multiplier)
    display_screen.blit(square, cur_px)
    pygame.display.flip()


def calculate_frame():
    cur_i = 0 - multiplier
    cur_j = 0 - multiplier

    global random_matrix
    new_matrix = numpy.copy(random_matrix)

    for i in range(height):
        cur_i = cur_i + multiplier
        for j in range(width):
            cur_col = random_matrix[i][j]
            cur_j = cur_j + multiplier
            square.fill(BLACK if cur_col == 0 else WHITE)
            cur_px = pygame.Rect(cur_i, cur_j, multiplier, multiplier)
            display_screen.blit(square, cur_px)
            update_cell(i, j, new_matrix)
        cur_j = 0 - multiplier
    pygame.display.flip()
    random_matrix = numpy.copy(new_matrix)


def update_cell(x, y, new_matrix):
    cell_alive = True if random_matrix[x][y] == 1 else False
    n1 = get_neighbour(x-1, y-1)
    n2 = get_neighbour(x, y-1)
    n3 = get_neighbour(x+1, y-1)
    n4 = get_neighbour(x+1, y)
    n5 = get_neighbour(x+1, y+1)
    n6 = get_neighbour(x, y+1)
    n7 = get_neighbour(x-1, y+1)
    n8 = get_neighbour(x-1, y)

    neighbours = [n1, n2, n3, n4, n5, n6, n7, n8]
    live_neighbours = 0
    dead_neighbours = 0

    for n in neighbours:
        if n == 0:
            dead_neighbours += 1
        else:
            live_neighbours += 1

    # NB: births and deaths occur simultaneously
    # Rules:
    # Any live cell with two or three live neighbours survives.
    # Any dead cell with three live neighbours becomes a live cell.
    # All other live cells die in the next generation. Similarly, all other dead cells stay dead.

    if cell_alive and (live_neighbours == 2 or live_neighbours == 3):
        new_matrix[x][y] = 1
    elif (not cell_alive) and live_neighbours == 3:
        new_matrix[x][y] = 1
    else:
        new_matrix[x][y] = 0


def get_neighbour(x1, y1):
    if x1 < 0 or x1 >= height:
        return 0
    elif y1 < 0 or y1 >= width:
        return 0
    else:
        return random_matrix[x1][y1]


def save_state():
    out_name = "state-{}.txt".format(int(time.time()))
    with open(out_name, 'w') as out_file:
        out_file.write("{0} {1} {2}\n".format(height, width, multiplier))
        for a in range(height):
            for b in range(width):
                if random_matrix[a][b] == 1:
                    out_file.write("{0} {1}\n".format(a, b))


def load_state(path):
    with open(path, 'r') as in_file:
        global height
        global width
        global multiplier
        global window_width
        global window_height
        global random_matrix

        params = in_file.readline().split(' ')
        height = int(params[0])
        width = int(params[1])
        multiplier = int(params[2])
        window_height = height*multiplier
        window_width = width*multiplier

        zero_matrix = numpy.random.randint(0, 1, (height, width))

        for line in in_file:
            coords = line.split(" ")
            x = int(coords[0])
            y = int(coords[1])
            zero_matrix[x][y] = 1

        random_matrix = zero_matrix


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('height', help='Specify the height', metavar='HEIGHT', default=100, nargs='?')
    parser.add_argument('width', help='Specify the width', metavar='WIDTH', default=100, nargs='?')
    parser.add_argument('multiplier', help='Specify the pixel multiplier', metavar='MULTIPLIER', default=1, nargs='?')
    parser.add_argument('-f', '--file', help='Specify the input file', metavar='FILE', required=False)
    args = parser.parse_args()

    filename = args.file

    if filename:
        if not os.path.isabs(filename):
            infile = os.path.join(sys.path[0], filename)
        load_state(filename)
    else:
        height = int(args.height)
        width = int(args.width)
        multiplier = int(args.multiplier)
        window_height = height * multiplier
        window_width = width * multiplier
        random_matrix = numpy.random.randint(0, 2, (height, width))
        save_state()

    pygame.init()

    display_screen = pygame.display.set_mode((window_height, window_width))
    pygame.display.set_caption("gameoflife")

    icon = pygame.image.load("icon.png").convert()
    pygame.display.set_icon(icon)

    square = pygame.Surface((multiplier, multiplier)).convert()
    calculate_frame()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                process_key_event(event.key)
            if event.type == pygame.MOUSEBUTTONUP:
                process_mouse_event(pygame.mouse.get_pos())

        if not PAUSED:
            calculate_frame()
