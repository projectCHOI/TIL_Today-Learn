import pygame
import sys

# 초기화
pygame.init()
WIDTH, HEIGHT = 800, 300
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini")
clock = pygame.time.Clock()

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (220, 40, 40)
GREEN = (40, 200, 60)

# 월드(지면) 설정
GROUND_Y = 240  # 지면 y좌표(선)
SCROLL_SPEED = 4  # 배경선 스크롤 느낌 (옵션)

# Dino(캐릭터) 설정
DINO_WIDTH, DINO_HEIGHT = 44, 50
DINO_DUCK_HEIGHT = 32  # 숙였을 때 높이
dino_x = 80
dino_y = GROUND_Y - DINO_HEIGHT
dino_vel_x = 0
dino_vel_y = 0

MOVE_SPEED = 6         # 좌우 이동 속도
GRAVITY = 1.2          # 중력
JUMP_POWER = -18       # 점프 초기 속도
on_ground = True
is_ducking = False
ground_offset = 0      # 지면 스크롤용 라인

def get_dino_rect():
    h = DINO_DUCK_HEIGHT if is_ducking else DINO_HEIGHT
    y = GROUND_Y - h if on_ground else (dino_y + (DINO_HEIGHT - h))
    return pygame.Rect(int(dino_x), int(y), DINO_WIDTH, h)

running = True

while running:
    dt = clock.tick(60) / 16.6667  # 60fps 기준 보정(대략 1.0)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # 좌우 이동
    dino_vel_x = 0
    if keys[pygame.K_LEFT]:
        dino_vel_x = -MOVE_SPEED
    if keys[pygame.K_RIGHT]:
        dino_vel_x = MOVE_SPEED

    # 점프: 지면에 있을 때만 위 화살표로 점프
    if keys[pygame.K_UP] and on_ground:
        dino_vel_y = JUMP_POWER
        on_ground = False

    # 숙이기: 아래 화살표 유지 시
    is_ducking = keys[pygame.K_DOWN] and on_ground

    # 수평 이동
    dino_x += dino_vel_x * dt
    dino_x = max(0, min(WIDTH - DINO_WIDTH, dino_x))

    # 수직(중력/점프)
    if not on_ground:
        dino_vel_y += GRAVITY * dt * 60  # 프레임 보정
        dino_y += dino_vel_y * dt

        # 바닥 충돌
        if dino_y >= GROUND_Y - DINO_HEIGHT:
            dino_y = GROUND_Y - DINO_HEIGHT
            dino_vel_y = 0
            on_ground = True
                
    # 공 위치 업데이트
    ball_x += ball_dx
    ball_y += ball_dy

    # 화면 경계와 충돌 시 튕기기
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_dx *= -1
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
        ball_dy *= -1

    # 화면 그리기
    win.fill(BLACK)
    pygame.draw.circle(win, ORANGE, (ball_x, ball_y), ball_radius)
    pygame.display.update()

pygame.quit()
sys.exit()