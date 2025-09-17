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

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)  # FPS 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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