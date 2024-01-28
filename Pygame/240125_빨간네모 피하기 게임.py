import pygame
import random
import time

# 게임 초기화
pygame.init()
width, height = 1000, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge the Falling Objects")

# 색상
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# 폰트 설정
pygame.font.init()
font = pygame.font.SysFont("comicsans", 40)

#플레이어 설정과 떨어지는 물체의 설정 값이 다르면, 타겟에 맞은 효과가 안 뜸,...
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
    if game_started:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # 키 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > player_speed:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
            player_pos[0] += player_speed

        # 물체가 떨어짐
        if enemy_pos[1] >= 0 and enemy_pos[1] < height:
            enemy_pos[1] += enemy_speed
        else:
            enemy_pos[0] = random.randint(0, width - enemy_size)
            enemy_pos[1] = 0
            score += 1

        # 충돌 감지
        if player_pos[0] < enemy_pos[0] < player_pos[0] + player_size or player_pos[0] < enemy_pos[0] + enemy_size < player_pos[0] + player_size:
            if player_pos[1] < enemy_pos[1] < player_pos[1] + player_size or player_pos[1] < enemy_pos[1] + enemy_size < player_pos[1] + player_size:
                run = False

        # 화면 업데이트
        win.fill(black)
        pygame.draw.rect(win, white, (player_pos[0], player_pos[1], player_size, player_size))
        pygame.draw.rect(win, red, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
        pygame.display.update()

        clock.tick(30)
    else:
        show_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True
                    start_time = time.time()

# 게임 종료 후 점수 표시 및 게임 종료 화면 호출
end_time = time.time()
show_game_over_screen()

# 게임 종료 후 이벤트 루프
game_over = True
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False

pygame.quit()