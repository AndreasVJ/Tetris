# This was one of the first programs I wrote, so be aware that the code is not very readable

import pygame
import random

pygame.init()
clock = pygame.time.Clock()
frame_rate = 30

screen = pygame.display.set_mode((697, 619))
pygame.display.set_caption("Tetris")

background = pygame.image.load("images/background.png")
blue = pygame.image.load("images/blue.png")
cyan = pygame.image.load("images/cyan.png")
green = pygame.image.load("images/green.png")
orange = pygame.image.load("images/orange.png")
purple = pygame.image.load("images/purple.png")
red = pygame.image.load("images/red.png")
yellow = pygame.image.load("images/yellow.png")

colors = [blue, cyan, green, orange, purple, red, yellow]

font20 = pygame.font.Font("freesansbold.ttf", 20)
score = 0
score_text = font20.render("score: " + str(score), True, (255, 255, 255))
lines_cleared = 0
lines_cleared_text = font20.render("lines: " + str(lines_cleared), True, (255, 255, 255))
level = 1
level_text = font20.render("level: " + str(level), True, (255, 255, 255))
rectangle = pygame.Surface((26, 26))

font26 = pygame.font.Font("freesansbold.ttf", 26)
font22 = pygame.font.Font("freesansbold.ttf", 23)


game_over_text = font26.render("GAME OVER", True, (255, 0, 0))
press_r_to_text = font22.render("Press \"r\" to", True, (255, 255, 255))
try_again_text = font22.render("try again", True, (255, 255, 255))

pause_text = font26.render("Game paused", True, (255, 255, 255))
press_any_key_text = font22.render("Press any key", True, (255, 255, 255))
to_continue_text = font22.render("to continue", True, (255, 255, 255))

piece_pos_list = [[[[0, 3], [1, 3], [1, 4], [1, 5]], [[0, 4], [0, 5], [1, 4], [2, 4]],
                   [[1, 3], [1, 4], [1, 5], [2, 5]], [[0, 4], [1, 4], [2, 3], [2, 4]]],

                  [[[1, 3], [1, 4], [1, 5], [1, 6]], [[0, 5], [1, 5], [2, 5], [3, 5]],
                   [[2, 3], [2, 4], [2, 5], [2, 6]], [[0, 4], [1, 4], [2, 4], [3, 4]]],

                  [[[0, 4], [0, 5], [1, 3], [1, 4]], [[0, 4], [1, 4], [1, 5], [2, 5]],
                   [[1, 4], [1, 5], [2, 3], [2, 4]], [[0, 3], [1, 3], [1, 4], [2, 4]]],

                  [[[0, 5], [1, 3], [1, 4], [1, 5]], [[0, 4], [1, 4], [2, 4], [2, 5]],
                   [[1, 3], [1, 4], [1, 5], [2, 3]], [[0, 3], [0, 4], [1, 4], [2, 4]]],

                  [[[0, 4], [1, 3], [1, 4], [1, 5]], [[0, 4], [1, 4], [1, 5], [2, 4]],
                   [[1, 3], [1, 4], [1, 5], [2, 4]], [[0, 4], [1, 3], [1, 4], [2, 4]]],

                  [[[0, 3], [0, 4], [1, 4], [1, 5]], [[0, 4], [1, 3], [1, 4], [2, 3]],
                   [[1, 3], [1, 4], [2, 4], [2, 5]], [[0, 5], [1, 4], [1, 5], [2, 4]]],

                  [[[0, 4], [0, 5], [1, 4], [1, 5]], [[0, 4], [0, 5], [1, 4], [1, 5]],
                   [[0, 4], [0, 5], [1, 4], [1, 5]], [[0, 4], [0, 5], [1, 4], [1, 5]]]]

grid = []


def make_game_grid():
    global grid
    grid = []
    for i in range(20):
        grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


make_game_grid()

grid_cords_x = []
for i in range(10):
    grid_cords_x.append(188 + i * 31)

grid_cords_y = []
for i in range(20):
    grid_cords_y.append(i * 31)

next_pieces = []
for i in range(3):
    next_pieces.append(random.randint(1, 7))

next_pieces_grid = []
for i in range(9):
    next_pieces_grid.append([0, 0, 0, 0])

next_pieces_grid_cords_x = []
for i in range(len(next_pieces_grid[0])):
    next_pieces_grid_cords_x.append(531 + i * 31)

next_pieces_grid_cords_y = []
for i in range(len(next_pieces_grid)):
    next_pieces_grid_cords_y.append(31 + i * 31)

stored_piece_grid = [[0, 0, 0, 0], [0, 0, 0, 0]]
stored_piece_grid_cords_x = [31, 62, 93, 124]
stored_piece_grid_cords_y = [31, 62]
stored_piece = 0

piece = 0
piece_pos = []
ghost_piece_pos = 0
rotation = 1
move_cooldown = 6
move_cooldown_count = move_cooldown + 1
move_down_count = 0
number_of_collisions = 0
move_down_count_limit = 60

new_piece = True
quit_program = False
swap_piece = False
swap_piece_cooldown = False
reset_screen = False
game_over = False
pause = False


def collision():
    global piece_pos
    for position in piece_pos[rotation]:
        if position[1] > 9 or position[1] < 0 or position[0] > 19:
            return True
        elif grid[position[0]][position[1]] > 0:
            return True


def update_next_pieces(number_of_updates):
    global next_pieces_grid
    for i in range(number_of_updates):
        for num in range(len(next_pieces) - 1):
            next_pieces[num] = next_pieces[num + 1]
        next_pieces[-1] = random.randint(1, 7)
        next_pieces_grid = []
        for num in range(9):
            next_pieces_grid.append([0, 0, 0, 0])
        for num in range(len(next_pieces)):
            for ind in piece_pos_list[next_pieces[num] - 1][0]:
                next_pieces_grid[ind[0] + num * 3][ind[1] - 3] = next_pieces[num]


def set_piece_pos():
    global piece_pos
    piece_pos = []
    for ind in range(len(piece_pos_list[piece - 1])):
        piece_pos.append([])
        for num in range(len(piece_pos_list[piece - 1][ind])):
            piece_pos[ind].append(piece_pos_list[piece - 1][ind][num][:])


def move(length_and_direction, zero_for_vertical_one_for_horizontal):
    for num in range(len(piece_pos)):
        for pos in piece_pos[num]:
            pos[zero_for_vertical_one_for_horizontal] += length_and_direction


def move_horizontal_with_cooldown_and_collision(length_and_direction):
    global move_cooldown_count
    if move_cooldown_count > move_cooldown:
        move(length_and_direction, 1)
    if move_cooldown_count == move_cooldown + 1:
        move_cooldown_count = 0
    move_cooldown_count += 2
    if collision():
        move(-length_and_direction, 1)


def draw_grid(rows, grid_type, grid_cords_list_x, grid_cords_list_y):
    for r in range(rows):
        for ind in range(len(grid_type[r])):
            if not grid_type[r][ind] == 0:
                screen.blit(colors[grid_type[r][ind] - 1],
                            (grid_cords_list_x[ind], grid_cords_list_y[r]))


while not quit_program:
    if reset_screen:
        new_piece = True
        game_over = False
        reset_screen = False
        stored_piece = 0
        stored_piece_grid = [[0, 0, 0, 0], [0, 0, 0, 0]]
        lines_cleared = 0
        score = 0
        level = 1
        move_down_count_limit = 60
        lines_cleared_text = font20.render("lines: " + str(lines_cleared), True, (255, 255, 255))
        score_text = font20.render("score: " + str(score), True, (255, 255, 255))
        level_text = font20.render("level: " + str(level), True, (255, 255, 255))
        make_game_grid()
        update_next_pieces(3)

    if new_piece:
        lines_cleared_score = 0
        rotation = 0
        swap_piece = False
        swap_piece_cooldown = False
        for n in range(len(grid)):
            for i in range(len(grid[n])):
                if grid[n][i] == 0:
                    break
                if i == len(grid[n]) - 1:
                    for row in reversed(range(1, n + 1)):
                        for value in range(len(grid[row])):
                            grid[row][value] = grid[row - 1][value]
                    for value in range(len(grid[0])):
                        grid[0][value] = 0
                    lines_cleared += 1
                    lines_cleared_score += 1
                    lines_cleared_text = font20.render("lines: " + str(lines_cleared), True, (255, 255, 255))
                    if lines_cleared == level * 10:
                        move_down_count_limit -= 6
                        level += 1
                        level_text = font20.render("level: " + str(level), True, (255, 255, 255))

        if not lines_cleared_score == 0:
            if not lines_cleared_score == 4:
                score += (200 * lines_cleared_score - 100) * level
            else:
                score += 800 * level
            score_text = font20.render("score: " + str(score), True, (255, 255, 255))
        piece = next_pieces[0]

        set_piece_pos()

        update_next_pieces(1)

        new_piece = False

        if collision():
            game_over = True

    for i in piece_pos[rotation]:
        grid[i[0]][i[1]] = 0

    if swap_piece and not swap_piece_cooldown:
        swap_piece_cooldown = True
        rotation = 0
        stored_piece_grid = [[0, 0, 0, 0], [0, 0, 0, 0]]
        if stored_piece == 0:
            stored_piece = piece
            piece = next_pieces[0]
            update_next_pieces(1)
        else:
            value_storage = stored_piece
            stored_piece = piece
            piece = value_storage
        set_piece_pos()
        for i in piece_pos_list[stored_piece - 1][0]:
            stored_piece_grid[i[0]][i[1] - 3] = stored_piece
        swap_piece = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quit_program = True

        if event.type == pygame.KEYDOWN:
            pause = False
            if event.key == pygame.K_r:
                reset_screen = True
            if event.key == pygame.K_p:
                if not game_over:
                    pause = True

            if not game_over:
                move_down_count -= 1
                if event.key == pygame.K_SPACE:
                    moves_down = -1
                    while not new_piece:
                        for i in piece_pos[rotation]:
                            i[0] += 1
                        moves_down += 1
                        if collision():
                            new_piece = True
                    for i in piece_pos[rotation]:
                        i[0] -= 1
                    score += moves_down * level
                    score_text = font20.render("score: " + str(score), True, (255, 255, 255))

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    rotation += 1
                    if rotation == 4:
                        rotation = 0
                    if collision():
                        move(-1, 1)
                    if collision():
                        move(-1, 1)
                    if collision():
                        move(3, 1)
                    if collision():
                        move(1, 1)
                    if collision():
                        move(-2, 1)
                        move(-1, 0)
                    if collision():
                        move(-1, 0)
                    if collision():
                        if rotation == 0:
                            rotation = 3
                        else:
                            rotation -= 1

                elif event.key == pygame.K_c:
                    swap_piece = True

    if not game_over:
        if not new_piece:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                move_horizontal_with_cooldown_and_collision(1)

            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                move_horizontal_with_cooldown_and_collision(-1)

            else:
                move_cooldown_count = move_cooldown + 1

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                move(1, 0)
                if collision():
                    move(-1, 0)

        ghost_piece_pos = 0

        if not pause:
            move_down_count += 2
        if move_down_count >= move_down_count_limit:
            move(1, 0)
            if collision():
                move(-1, 0)
                new_piece = True
                number_of_collisions += 1
            move_down_count = 0

        while True:
            if collision():
                break
            move(1, 0)
            ghost_piece_pos += 1
        move(- ghost_piece_pos, 0)
        if not ghost_piece_pos == 0:
            ghost_piece_pos -= 1

        for i in piece_pos[rotation]:
            grid[i[0]][i[1]] = piece

    screen.fill((0, 0, 0))
    screen.blit(background, (186, 0))

    # Ghost pieces
    for i in piece_pos[rotation]:
        screen.blit(colors[piece - 1], (grid_cords_x[i[1]], grid_cords_y[i[0] + ghost_piece_pos]))
        screen.blit(rectangle, (grid_cords_x[i[1]] + 2, grid_cords_y[i[0] + ghost_piece_pos] + 2))

    draw_grid(20, grid, grid_cords_x, grid_cords_y)
    draw_grid(len(next_pieces_grid), next_pieces_grid, next_pieces_grid_cords_x, next_pieces_grid_cords_y)
    draw_grid(len(stored_piece_grid), stored_piece_grid, stored_piece_grid_cords_x, stored_piece_grid_cords_y)

    screen.blit(lines_cleared_text, (35, 540))
    screen.blit(score_text, (540, 540))
    screen.blit(level_text, (35, 500))

    if game_over:
        screen.blit(game_over_text, (10, 250))
        screen.blit(press_r_to_text, (30, 290))
        screen.blit(try_again_text, (45, 315))

    elif pause:
        screen.blit(pause_text, (5, 250))
        screen.blit(press_any_key_text, (15, 290))
        screen.blit(to_continue_text, (30, 315))

    clock.tick(frame_rate)
    pygame.display.update()
