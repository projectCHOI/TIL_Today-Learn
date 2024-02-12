import pygame
import random
import time

# 게임 초기화 및 설정
pygame.init()
width, height = 1000, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge the Falling Objects")

# 색상 및 폰트 설정
black, white, red = (0, 0, 0), (255, 255, 255), (255, 0, 0)
pygame.font.init()
font = pygame.font.SysFont("comicsans", 40)

# 플레이어 및 떨어지는 물체 설정
player_size, player_speed = 50, 10
enemy_speed = 10

# 시계 설정
clock = pygame.time.Clock()

# 게임 변수 초기화 함수
def initialize_game():
    global player_pos, enemies, score, start_time, game_started, game_over
    player_pos = [width / 2, height - 2 * player_size]
    # 초기 적 리스트를 생성할 때, 각 적의 크기를 랜덤으로 설정합니다.
    enemies = [{'pos': [random.randint(0, width - random.randint(10, 50)), 0], 'direction': [0, enemy_speed], 'size': random.randint(10, 50)} for _ in range(5)]
    score = 0
    start_time = time.time()
    game_started = False
    game_over = False

# 새로운 물체를 추가하는 함수
def add_enemy():
    enemy_size = random.randint(10, 50)  # 랜덤한 크기로 적을 생성합니다.
    edge = random.choice(['top', 'left', 'right'])
    if edge == 'top':
        new_enemy = {'pos': [random.randint(0, width - enemy_size), 0], 'direction': [0, enemy_speed], 'size': enemy_size}
    elif edge == 'left':
        new_enemy = {'pos': [0, random.randint(0, height - enemy_size)], 'direction': [enemy_speed, 0], 'size': enemy_size}
    else:  # edge == 'right'
        new_enemy = {'pos': [width - enemy_size, random.randint(0, height - enemy_size)], 'direction': [-enemy_speed, 0], 'size': enemy_size}
    enemies.append(new_enemy)

# 시작 화면 및 게임 종료 화면 함수
def show_start_screen():
    win.fill(black)
    title = font.render("Dodge the Falling Objects", True, white)
    start_message = font.render("Start : Spacebar", True, white)
    title_rect = title.get_rect(center=(width / 2, height / 2 - 40))
    start_message_rect = start_message.get_rect(center=(width / 2, height / 2 + 40))
    win.blit(title, title_rect)
    win.blit(start_message, start_message_rect)

def show_game_over_screen():
    win.fill(black)
    game_over_message = font.render("Game Over", True, white)
    score_message = font.render(f"Playtime : {time.time() - start_time:.2f} seconds", True, white)
    game_over_message_rect = game_over_message.get_rect(center=(width / 2, height / 2 - 40))
    score_message_rect = score_message.get_rect(center=(width / 2, height / 2 + 20))
    win.blit(game_over_message, game_over_message_rect)
    win.blit(score_message, score_message_rect)

# 게임 변수 초기화
initialize_game()

# 게임 루프
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if not game_started:
        show_start_screen()
        if keys[pygame.K_SPACE]:
            game_started = True
            start_time = time.time()
    elif game_over:
        show_game_over_screen()
        if keys[pygame.K_SPACE]:
            initialize_game()
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
        if len(enemies) < (time.time() - start_time) // 10 + 1:
            add_enemy()

        win.fill(black)  # 화면 지우기

        # 물체 업데이트, 충돌 검사 및 그리기
        for enemy in enemies[:]:
            enemy['pos'][0] += enemy['direction'][0]
            enemy['pos'][1] += enemy['direction'][1]
            pygame.draw.rect(win, red, (enemy['pos'][0], enemy['pos'][1], enemy['size'], enemy['size']))
            # 화면 밖으로 나가면 리셋
            if enemy['pos'][0] < 0 or enemy['pos'][0] > width or enemy['pos'][1] < 0 or enemy['pos'][1] > height:
                enemies.remove(enemy)
                score += 1
            # 충돌 검사
            if player_pos[0] < enemy['pos'][0] + enemy['size'] and player_pos[0] + player_size > enemy['pos'][0] and player_pos[1] < enemy['pos'][1] + enemy['size'] and player_pos[1] + player_size > enemy['pos'][1]:
                game_over = True
                end_time = time.time()

        # 플레이어 그리기
        pygame.draw.rect(win, white, (player_pos[0], player_pos[1], player_size, player_size))

        # 시간 표시
        if not game_over:
            elapsed_time = time.time() - start_time
            time_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, white)
            win.blit(time_text, (10, 10))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
