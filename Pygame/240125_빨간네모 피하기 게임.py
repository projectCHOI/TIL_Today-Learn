import pygame
import random
import time

# 게임 초기화 및 설정
pygame.init()
width, height = 1000, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge the Falling Objects")

# 색상 설정
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# 폰트 설정
pygame.font.init()
font = pygame.font.SysFont("comicsans", 40)

# 플레이어 설정
player_size = 50
player_speed = 40

# 떨어지는 물체 설정
enemy_size = 50
enemy_speed = 40

# 게임 변수 초기화 함수
def initialize_game():
    global player_pos, enemy_pos, score, start_time, game_started, game_over
    player_pos = [width / 2, height - 2 * player_size]
    enemy_pos = [random.randint(0, width - enemy_size), 0]
    score = 0
    start_time = 0
    game_started = False
    game_over = False

# 시계 설정
clock = pygame.time.Clock()

# 물체의 초기 위치와 방향 설정 함수
def reset_enemy():
    global enemy_pos, enemy_direction, enemy_size
    enemy_size = random.randint(10, 50)  # 물체 크기를 10에서 50 사이의 랜덤한 값으로 설정
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    
    if edge == 'top':
        enemy_pos = [random.randint(0, width - enemy_size), 0]
        enemy_direction = [0, enemy_speed]
    elif edge == 'bottom':
        enemy_pos = [random.randint(0, width - enemy_size), height - enemy_size]
        enemy_direction = [0, -enemy_speed]
    elif edge == 'left':
        enemy_pos = [0, random.randint(0, height - enemy_size)]
        enemy_direction = [enemy_speed, 0]
    else:  # edge == 'right'
        enemy_pos = [width - enemy_size, random.randint(0, height - enemy_size)]
        enemy_direction = [-enemy_speed, 0]


# 게임 변수 초기화 함수
def initialize_game():
    global player_pos, enemy_pos, score, start_time, game_started, game_over
    player_pos = [width / 2, height - 2 * player_size]
    enemy_pos = [random.randint(0, width - enemy_size), 0]
    score = 0
    start_time = 0
    game_started = False
    game_over = False
    reset_enemy() # 물체의 초기 위치와 방향 설정

# 게임 변수 초기화
initialize_game()

# 시계 설정
clock = pygame.time.Clock()

# 플레이어 설정
player_size = 50
player_pos = [width / 2, height - 2 * player_size]
player_speed = 10

# 떨어지는 물체 설정
enemy_size = 50
enemy_pos = [random.randint(0, width - enemy_size), 0]
enemy_speed = 10


clock = pygame.time.Clock()

# 게임 변수
score = 0
game_started = False
# game_over = False

# 시작 화면 함수
def show_start_screen():
    win.fill(black)
    title = font.render("A red box descends from the sky", True, white)
    start_message = font.render("Start : Spacebar", True, white)

    # 타이틀과 시작 메시지의 중앙 정렬
    title_rect = title.get_rect(center=(width / 2, height / 2 - 40))
    start_message_rect = start_message.get_rect(center=(width / 2, height / 2 + 40))

    win.blit(title, title_rect)
    win.blit(start_message, start_message_rect)
    pygame.display.update()

# 게임 종료 화면 함수
def show_game_over_screen():
    win.fill(black)
    game_over_message = font.render("Game Over", True, white)
    score_message = font.render(f"Playtime : {end_time - start_time:.2f} seconds", True, white)

    # 게임 오버 메시지와 점수 메시지의 중앙 정렬
    game_over_message_rect = game_over_message.get_rect(center=(width / 2, height / 2 - 40))
    score_message_rect = score_message.get_rect(center=(width / 2, height / 2 + 20))

    win.blit(game_over_message, game_over_message_rect)
    win.blit(score_message, score_message_rect)
    pygame.display.update()
    
# 게임 루프
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()  # 현재 눌려있는 키 상태를 가져옴

    if game_over:
        # 게임 오버 상태에서의 이벤트 처리
        if keys[pygame.K_SPACE]:
            initialize_game()

    elif not game_started:
        # 게임 시작 화면에서의 이벤트 처리
        if keys[pygame.K_SPACE]:
            game_started = True
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

    # 게임 로직
    if game_started and not game_over:
        # 물체 이동
        enemy_pos[0] += enemy_direction[0]
        enemy_pos[1] += enemy_direction[1]

        # 물체가 화면 밖으로 나갔는지 확인
        if (enemy_pos[0] < 0 or enemy_pos[0] > width or
            enemy_pos[1] < 0 or enemy_pos[1] > height):
            reset_enemy()  # 새로운 물체 위치와 방향 설정
            score += 1

        # 충돌 감지
        if player_pos[0] < enemy_pos[0] + enemy_size and player_pos[0] + player_size > enemy_pos[0]:
            if player_pos[1] < enemy_pos[1] + enemy_size and player_pos[1] + player_size > enemy_pos[1]:
                end_time = time.time()
                game_over = True

        # 화면 업데이트
        win.fill(black)
        pygame.draw.rect(win, white, (player_pos[0], player_pos[1], player_size, player_size))
        pygame.draw.rect(win, red, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

    # 게임 진행 시간 표시
    if game_started and not game_over:
        elapsed_time = time.time() - start_time
        time_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, white)
        win.blit(time_text, (10, 10))  # 상단에 시간 표시

    # 플레이어와 물체 그리기
    pygame.draw.rect(win, white, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.draw.rect(win, red, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

    # 게임 시작 화면 또는 게임 오버 화면 표시
    if game_over:
        show_game_over_screen()
    elif not game_started:
        show_start_screen()

    pygame.display.update()
    clock.tick(30)

pygame.quit()