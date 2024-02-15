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
player_speed = 10  # 플레이어 속도 조정

# 음악 파일 로드
pygame.mixer.music.load('C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/TIL_Today-Learn/Pygame/240211_red box_music.wav')
pygame.mixer.music.play(-1)  # -1은 음악을 무한 반복 재생

clock = pygame.time.Clock()
score = 0
game_started = False
game_over = False

def initialize_game():
    global player_pos, enemies, score, start_time, game_started, game_over
    player_pos = [width / 2, height - 2 * player_size]
    enemies = []  # 초기 적 리스트 설정
    score = 0
    start_time = time.time()
    game_started = False
    game_over = False
    # pygame.mixer.music.stop()  # 음악 관련 코드는 필요에 따라 주석 해제

def add_enemy():
    global enemies
    enemy_size = random.randint(10, 50)
    enemy_speed = random.randint(10, 30)  # 랜덤 속도 설정
    edge = random.choice(['top', 'left', 'right'])
    if edge == 'top':
        new_enemy = {'pos': [random.randint(0, width - enemy_size), 0], 'direction': [0, enemy_speed], 'size': enemy_size}
    elif edge == 'left':
        new_enemy = {'pos': [0, random.randint(0, height - enemy_size)], 'direction': [enemy_speed, 0], 'size': enemy_size}
    else:
        new_enemy = {'pos': [width - enemy_size, random.randint(0, height - enemy_size)], 'direction': [-enemy_speed, 0], 'size': enemy_size}
    enemies.append(new_enemy)

def show_start_screen():
    win.fill(black)
    title = font.render("A red box descends from the sky", True, white)
    start_message = font.render("Start : Spacebar", True, white)
    title_rect = title.get_rect(center=(width / 2, height / 2 - 40))
    start_message_rect = start_message.get_rect(center=(width / 2, height / 2 + 40))
    win.blit(title, title_rect)
    win.blit(start_message, start_message_rect)
    pygame.display.update()

def show_game_over_screen():
    win.fill(black)
    game_over_message = font.render("Game Over", True, white)
    score_message = font.render(f"Score: {score:.1f}", True, white)
    game_over_message_rect = game_over_message.get_rect(center=(width / 2, height / 2 - 40))
    score_message_rect = score_message.get_rect(center=(width / 2, height / 2 + 20))
    win.blit(game_over_message, game_over_message_rect)
    win.blit(score_message, score_message_rect)
    pygame.display.update()

initialize_game()

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
            if len(enemies) < (time.time() - start_time) // 10 + 1:
                add_enemy()

            win.fill(black)
            for enemy in list(enemies):
                enemy['pos'][0] += enemy['direction'][0]
                enemy['pos'][1] += enemy['direction'][1]
                
                pygame.draw.rect(win, red, (enemy['pos'][0], enemy['pos'][1], enemy['size'], enemy['size']))

                if enemy['pos'][0] < 0 or enemy['pos'][0] > width or enemy['pos'][1] < 0 or enemy['pos'][1] > height:
                    enemies.remove(enemy)
                    score += 1
                if player_pos[0] < enemy['pos'][0] + enemy['size'] and player_pos[0] + player_size > enemy['pos'][0]:
                    if player_pos[1] < enemy['pos'][1] + enemy['size'] and player_pos[1] + player_size > enemy['pos'][1]:
                        game_over = True

            pygame.draw.rect(win, white, (player_pos[0], player_pos[1], player_size, player_size))
            time_text = font.render(f"Time: {time.time() - start_time:.1f} seconds", True, white)
            win.blit(time_text, (10, 10))


    if game_over:
        show_game_over_screen()
    elif not game_started:
        show_start_screen()

    pygame.display.update()
    clock.tick(30)

pygame.quit()