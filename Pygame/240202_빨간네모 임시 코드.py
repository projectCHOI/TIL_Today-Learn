import pygame
import random
import time

# 게임 초기화 및 설정
pygame.init()
pygame.font.init()
pygame.mixer.init()

width, height = 1000, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge the Falling Objects")

# 색상 설정
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# 폰트 설정
font = pygame.font.SysFont("comicsans", 40)

# 플레이어 설정
player_size = 30
player_speed = 10
player_pos = [width / 2, height - 2 * player_size]

# 떨어지는 물체 설정
enemy_speed = 10  # 기본 속도 설정

# 시계 설정
clock = pygame.time.Clock()

# 게임 변수 및 함수 초기화
game_started = False
game_over = False
score = 0
enemies = []

def initialize_game():
    global player_pos, enemies, score, start_time, game_started, game_over
    player_pos = [width / 2, height - 2 * player_size]
    enemies = [{'pos': [random.randint(0, width - enemy_size), 0], 'direction': [0, enemy_speed], 'size': random.randint(10, 50)}]
    score = 0
    start_time = time.time()
    game_started = False
    game_over = False
    pygame.mixer.music.stop()  # 이전 게임의 음악 중지

def add_enemy():
    enemy_size = random.randint(10, 50)
    enemy_speed = random.randint(10, 30)  # 랜덤한 속도 설정
    edge = random.choice(['top', 'left', 'right'])
    if edge == 'top':
        new_enemy = {'pos': [random.randint(0, width - enemy_size), 0], 'direction': [0, enemy_speed], 'size': enemy_size}
    elif edge == 'left':
        new_enemy = {'pos': [0, random.randint(0, height - enemy_size)], 'direction': [enemy_speed, 0], 'size': enemy_size}
    else:  # edge == 'right'
        new_enemy = {'pos': [width - enemy_size, random.randint(0, height - enemy_size)], 'direction': [-enemy_speed, 0], 'size': enemy_size}
    enemies.append(new_enemy)

def show_start_screen():
    win.fill(black)
    title = font.render("A red box descends from the sky", True, white)
    start_message = font.render("Start : Spacebar", True, white)
    win.blit(title, (width / 2 - title.get_width() / 2, height / 2 - 40))
    win.blit(start_message, (width / 2 - start_message.get_width() / 2, height / 2 + 40))
    pygame.display.update()

def show_game_over_screen():
    win.fill(black)
    game_over_message = font.render("Game Over", True, white)
    score_message = font.render(f"Playtime : {time.time() - start_time:.2f} seconds", True, white)
    win.blit(game_over_message, (width / 2 - game_over_message.get_width() / 2, height / 2 - 40))
    win.blit(score_message, (width / 2 - score_message.get_width() / 2, height / 2 + 20))
    pygame.display.update()

# 게임 루프
initialize_game()  # 게임 변수 초기화
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
            pygame.mixer.music.play(-1)  # 게임 시작시 음악 재생
            start_time = time.time()
    else:
        # 플레이어 이동 처리
        if keys[pygame.K_LEFT] and player_pos[0] > player_speed:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > player_speed:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < height - player_size:
            player_pos[1] += player_speed

        # 시간에 따라 새로운 물체 추가
        if game_started and not game_over and len(enemies) < (time.time() - start_time) // 10 + 1:
            add_enemy()

        win.fill(black)  # 화면 지우기
        # 물체 업데이트 및 충돌 검사 및 그리기
        for enemy in enemies[:]:  # 리스트 복사하여 반복 중 수정 가능
            enemy['pos'][0] += enemy['direction'][0]
            enemy['pos'][1] += enemy['direction'][1]
            pygame.draw.rect(win, red, (enemy['pos'][0], enemy['pos'][1], enemy['size'], enemy['size']))
            if enemy['pos'][0] < 0 or enemy['pos'][0] > width or enemy['pos'][1] < 0 or enemy['pos'][1] > height:
                enemies.remove(enemy)
                score += 1
            if player_pos[0] < enemy['pos'][0] + enemy['size'] and player_pos[0] + player_size > enemy['pos'][0] and player_pos[1] < enemy['pos'][1] + enemy['size'] and player_pos[1] + player_size > enemy['pos'][1]:
                game_over = True
                pygame.mixer.music.stop()  # 게임 오버시 음악 중지

        # 플레이어 그리기
        pygame.draw.rect(win, white, (player_pos[0], player_pos[1], player_size, player_size))

        # 게임 진행 시간 표시
        if not game_over:
            elapsed_time = time.time() - start_time
            time_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, white)
            win.blit(time_text, (10, 10))

    # 화면 업데이트
    if game_over:
        show_game_over_screen()
    elif not game_started:
        show_start_screen()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
