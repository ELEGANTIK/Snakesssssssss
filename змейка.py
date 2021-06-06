import pygame
import pygame_menu
from pygame.locals import *
import random


pygame.init()

screen_height = 600
screen_width = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

#определение шрифта
font = pygame.font.SysFont(None,40)

#установка прямоугольника для опции "Воспроизвести снова"
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)
over_rect = Rect(screen_width // 2 - 80, screen_height // 2 - 60, 160, 50)

cell_size = 10
update_snake = 0
food = [0, 0]
new_food = True
new_piece = [0, 0]
game_over = False
score= 0
clicked = False
FPS = 20

#настройка змейки
snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
snake_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size])
snake_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 2])
snake_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 3])
direction = 1 #1 это вверх, 2 это вправа, 3 это вниз, 4 это влево

#определение игровых переменных
bg = (255, 200, 150)
body_inner = (50, 175, 25)
body_outer = (100, 100, 200)
food_col = (200, 50, 50)
blue = (0, 0, 255)
red = (255, 0, 0)

def draw_screen():
    screen.fill(bg)

def draw_score():
    score_txt = 'Score: ' + str(score)
    score_img = font.render(score_txt, True, blue)
    screen.blit(score_img, (0, 0))

def check_game_over(game_over):
    head_count = 0
    for x in snake_pos:
        if snake_pos[0] == x and head_count > 0:
            game_over = True
        head_count += 1

    if snake_pos[0][0] < 0 or snake_pos[0][0] > screen_width or snake_pos[0][1] < 0 or snake_pos[0][1] > screen_height:
        game_over = True

    return game_over

def draw_game_over():
    over_text = "Game Over!"
    over_img = font.render(over_text, True, blue)
    pygame.draw.rect(screen, red, over_rect)
    screen.blit(over_img, (screen_width // 2 - 80, screen_height // 2 - 50))

    again_text = "Play Again?"
    again_img = font.render(again_text, True, blue)
    pygame.draw.rect(screen, red, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))
def start_the_game():
    global new_food, food, snake_pos, game_over, update_snake, direction, clicked, score, FPS
    run = True
    clock = pygame.time.Clock()
    set_difficulty(selector.get_value()[0][0],selector.get_value()[0][1])
    while run:
        clock.tick(FPS)
        draw_screen()
        draw_score()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 3:
                    direction = 1
                if event.key == pygame.K_RIGHT and direction != 4:
                    direction = 2
                if event.key == pygame.K_DOWN and direction != 1:
                    direction = 3
                if event.key == pygame.K_LEFT and direction != 2:
                    direction = 4
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                pos = pygame.mouse.get_pos()
                if again_rect.collidepoint(pos):
                    direction = 1
                    game_over = False
                    update_snake = 0
                    food = [0, 0]
                    new_food = True
                    new_piece = [0, 0]
                    snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
                    snake_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size])
                    snake_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 2])
                    snake_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 3])
                    direction = 1
                    score = 0
                elif over_rect.collidepoint(pos):
                    pygame.quit()

        if new_food == True:
            new_food = False
            food[0] = cell_size * random.randint(0, (screen_width / cell_size) - 1)
            food[1] = cell_size * random.randint(0, (screen_height / cell_size) - 1)

        pygame.draw.rect(screen, food_col, (food[0], food[1], cell_size, cell_size))

        if snake_pos[0] == food:
            new_food = True
            new_piece = list(snake_pos[-1])
            if direction == 1:
                new_piece[1] += cell_size
            if direction == 3:
                new_piece[1] -= cell_size
            if direction == 2:
                new_piece[0] -= cell_size
            if direction == 4:
                new_piece[0] += cell_size

            snake_pos.append(new_piece)
            score += 1

        if game_over == False:

            update_snake = 0
            snake_pos = snake_pos[-1:] + snake_pos[:-1]
            if direction == 1:
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] - cell_size
            if direction == 3:
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] + cell_size
            if direction == 2:
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] + cell_size
            if direction == 4:
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] - cell_size
            game_over = check_game_over(game_over)

        if game_over == True:
            draw_game_over()

        head = 1
        for x in snake_pos:

            if head == 0:
                pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
                pygame.draw.rect(screen, body_inner, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
            if head == 1:
                pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
                pygame.draw.rect(screen, (255,0,0), (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
                head = 0

        pygame.display.update()

        update_snake += 1


def set_difficulty(value, difficulty):
    global FPS
    FPS = difficulty

menu = pygame_menu.Menu(300, 400, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='None')
selector = menu.add.selector('Difficulty :', [('Hard', 60),('Normal', 40), ('Easy', 20)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen)