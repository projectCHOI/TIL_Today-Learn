import pygame
import random
import time

pygame.init()
width, height = 1000, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge the Falling Objects")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

pygame.font.init()
font = pygame.font.SysFont("comicsans", 40)

player_size = 50
player_speed = 10
player_pos = [width / 2, height - 2 * player_size]

enemy_speed = 10
enemies = []

clock = pygame.time.Clock()

score = 0
game_started = False
game_over = False

def add_enemy():
    enemy_size = random.randint(10, 50)
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    if edge == 'top':
        enemy_pos = [random.randint(0, width - enemy_size), 0]
        enemy_direction = [0, enemy_speed]
    elif edge == 'bottom':
        enemy_pos = [random.randint(0, width - enemy_size), height]
        enemy_direction = [0, -enemy_speed]
    elif edge == 'left':
        enemy_pos = [0, random.randint(0, height - enemy_size)]
        enemy_direction = [enemy_speed, 0]
    else:  # edge == 'right'
        enemy_pos = [width, random.randint(0, height - enemy_size)]
        enemy_direction = [-enemy_speed, 0]
    enemies.append({"pos": enemy_pos, "direction": enemy_direction, "size": enemy_size})

def initialize_game():
    global player_pos, enemies, score, start_time, game_started, game_over
    player_pos = [width / 2, height - 2 * player_size]
    enemies = []
    add_enemy()
    score = 0
    start_time = time.time()
    game_started = False
    game_over = False

initialize_game()

def show_start_screen():
    # (Show start screen logic)

def show_game_over_screen():
    # (Show game over screen logic)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if game_over:
        if keys[pygame.K_SPACE]:
            initialize_game()

    elif not game_started:
        if keys[pygame.K_SPACE]:
            game_started = True
            start_time = time.time()

    else:
        if keys[pygame.K_LEFT] and player_pos[0] > player_speed:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > player_speed:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < height - player_size:
            player_pos[1] += player_speed

        if game_started and not game_over:
            current_time = time.time()
            if (current_time - start_time) // 10 > len(enemies) - 1:
                add_enemy()

            for enemy in enemies:
                enemy["pos"][0] += enemy["direction"][0]
                enemy["pos"][1] += enemy["direction"][1]
                if (enemy["pos"][0] < -50 or enemy["pos"][0] > width or
                        enemy["pos"][1] < -50 or enemy["pos"][1] > height):
                    enemies.remove(enemy)
                    add_enemy()
                    score += 1

                # 충돌 검사
                if player_pos[0] < enemy["pos"][0] + enemy["size"] and player_pos[0] + player_size > enemy["pos"][0]:
                    if player_pos[1] < enemy["pos"][1] + enemy["size"] and player_pos[1] + player_size > enemy["pos"][1]:
                        end_time = time.time()
                        game_over = True

        win.fill(black)
        pygame.draw.rect(win, white, (player_pos[0], player_pos[1], player_size, player_size))
        for enemy in enemies:
            pygame.draw.rect(win, red, (enemy["pos"][0], enemy["pos"][1], enemy["size"], enemy["size"]))

    if game_started and not game_over:
        elapsed_time = time.time() - start_time
        time_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, white)
        win.blit(time_text, (10, 10))

    if game_over:
        show_game_over_screen()
    elif not game_started:
        show_start_screen()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
