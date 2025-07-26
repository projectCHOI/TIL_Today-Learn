import pygame
import sys

# 초기화
pygame.init()
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball")

# 색상
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

# 공 설정
ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 4   # x 방향 속도
ball_dy = 3   # y 방향 속도

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