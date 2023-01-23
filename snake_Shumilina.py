import pygame
import sys
import time
from random import randrange

difficulty = 8

# размеры окна приложения
cols = 50
rows = 50
head = 10
max_x = cols * head
max_y = rows * head

pygame.init()
pygame.display.set_caption('Игра змейка')
game_window = pygame.display.set_mode((max_x, max_y))

clock = pygame.time.Clock()

# змея
snake_head = [100, 100]
snake_body = [snake_head]
# яблоко
food_pos = [randrange(1, (max_x//10)) * 10, randrange(1, (max_y//10)) * 10]

direction = 'right'
change_to = direction

score = 0

# сопровождение: заставка и музыка
img = pygame.image.load('zastavka-temnii.jpg').convert()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play()
sound1 = pygame.mixer.Sound('apple_bite.mp3')
game_over_sound = pygame.mixer.Sound('game over.mp3')

# Финальный экран
def game_over():
    my_font = pygame.font.SysFont('isocpeur', 40, bold=True, italic=True)
    game_over_surface = my_font.render('Игра окончена!', True, pygame.Color('orange'))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (max_x/2, max_y/3)
    game_window.fill(pygame.Color('black'))
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, pygame.Color('orange'), 'isocpeur', 30)
    pygame.display.flip()

    pygame.mixer.music.stop()
    game_over_sound.play()

    time.sleep(game_over_sound.get_length())
    pygame.quit()
    sys.exit()


# Счет на экране
def show_score(num_display, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Ваш счет : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if num_display == 1:
        score_rect.topleft = (15, 15)
    else:
        score_rect.midtop = (max_x//2, max_y//2)
    game_window.blit(score_surface, score_rect)


# Основной цикл приложения
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'down': change_to = 'up'
            if event.key == pygame.K_DOWN and direction != 'up': change_to = 'down'
            if event.key == pygame.K_LEFT and direction != 'right': change_to = 'left'
            if event.key == pygame.K_RIGHT and direction != 'left': change_to = 'right'
            if event.key == pygame.K_1: pygame.mixer.music.pause()
            if event.key == pygame.K_2: pygame.mixer.music.play()
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # уточним, что направление движения допустимо
    if change_to == 'up':
        direction = 'up'
        snake_head[1] -= head
    if change_to == 'down':
        direction = 'down'
        snake_head[1] += head
    if change_to == 'left':
        direction = 'left'
        snake_head[0] -= head
    if change_to == 'right':
        direction = 'right'
        snake_head[0] += head

    # Изменение тела змеи при движении
    snake_body.insert(0, list(snake_head))
    if snake_head == food_pos:
        score += 1
        sound1.play()
        food_pos = [randrange(1, (max_x // 10)) * 10, randrange(1, (max_y // 10)) * 10]
    else:
        snake_body.pop()

    game_window.blit(img, (0, 0))
    [pygame.draw.rect(game_window, pygame.Color('green'),
                      (*pos, head, head)) for pos in snake_body]
    pygame.draw.rect(game_window, pygame.Color('red'), (*food_pos, head, head))

    # проверка на выход за границы экрана
    if snake_head[0] < 0 or snake_head[0] > max_x-head \
            or snake_head[1] < 0 or snake_head[1] > max_y-head:
        game_over()
    # змея пересекает себя
    [game_over() for block in snake_body[1:] if snake_head == block]

    show_score(1, pygame.Color('orange'), 'isocpeur', 30)
    pygame.display.update()
    clock.tick(difficulty)
