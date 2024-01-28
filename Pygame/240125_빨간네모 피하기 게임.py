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
player_speed = 10

# 떨어지는 물체 설정
enemy_size = 50
enemy_speed = 10

# 게임 변수 초기화 함수
def initialize_game():
    global player_pos, enemy_pos, score, start_time, game_started, game_over
    player_pos = [width / 2, height - 2 * player_size]
    enemy_pos = [random.randint(0, width - enemy_size), 0]
    score = 0
    start_time = 0
    game_started = False
    game_over = False

# 게임 변수 초기화
initialize_game()

# 시계 설정
clock = pygame.time.Clock()

# 게임 변수 초기화 함수
def initialize_game():
    global player_pos, enemy_pos, score, start_time, game_started, game_over
    player_pos = [width / 2, height - 2 * player_size]
    enemy_pos = [random.randint(0, width - enemy_size), 0]
    score = 0
    start_time = 0
    game_started = False
    game_over = False

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

        if game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                initialize_game()

        elif not game_started:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_started = True
                start_time = time.time()

        else:
            # 키 입력 처리
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player_pos[0] > player_speed:
                    player_pos[0] -= player_speed
                elif event.key == pygame.K_RIGHT and player_pos[0] < width - player_size:
                    player_pos[0] += player_speed

    # 게임 로직
    if game_started and not game_over:
        # 물체가 떨어짐
        enemy_pos[1] += enemy_speed
        if enemy_pos[1] > height:
            enemy_pos[0] = random.randint(0, width - enemy_size)
            enemy_pos[1] = 0
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

    elif game_over:
        show_game_over_screen()

    else:
        show_start_screen()

    pygame.display.update()
    clock.tick(30)

pygame.quit()