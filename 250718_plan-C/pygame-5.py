import pygame
import sys

# 초기화
pygame.init()
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")

# 색상
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)

# 플레이어 설정
player_width, player_height = 40, 50
player_x, player_y = 100, HEIGHT - player_height - 50
player_speed = 5
player_vel_y = 0
gravity = 0.5
jump_power = -10
on_ground = False

# 플랫폼 설정
platforms = [
    pygame.Rect(0, HEIGHT - 40, WIDTH, 40),      # 바닥
    pygame.Rect(150, 300, 100, 20),
    pygame.Rect(300, 220, 120, 20),
    pygame.Rect(480, 150, 100, 20),
]

# 게임 루프
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    win.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and on_ground:  # 점프는 땅 위에서만 가능
        player_vel_y = jump_power
        on_ground = False

    # 중력 적용
    player_vel_y += gravity
    player_y += player_vel_y

    # 플레이어 직사각형 객체
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # 플랫폼 충돌 처리
    on_ground = False
    for plat in platforms:
        if player_rect.colliderect(plat):
            # 플레이어가 위에서 떨어질 때만 착지
            if player_vel_y > 0 and player_rect.bottom - player_vel_y <= plat.top:
                player_y = plat.top - player_height
                player_vel_y = 0
                on_ground = True

    # 화면 밖으로 나가지 않도록
    if player_x < 0: player_x = 0
    if player_x > WIDTH - player_width: player_x = WIDTH - player_width
    if player_y > HEIGHT:  # 화면 아래로 떨어지면 리셋
        player_x, player_y = 100, HEIGHT - player_height - 50
        player_vel_y = 0

    # 그리기
    pygame.draw.rect(win, BLUE, (player_x, player_y, player_width, player_height))  # 플레이어
    for plat in platforms:
        pygame.draw.rect(win, GREEN, plat)  # 플랫폼

    pygame.display.update()

pygame.quit()
sys.exit()