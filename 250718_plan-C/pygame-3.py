import pygame
import sys

# 초기화
pygame.init()
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Clone")

# 색상
WHITE = (255, 255, 255)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)

# 패들 설정
paddle_width, paddle_height = 100, 10
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 30
paddle_speed = 8

# 공 설정
ball_radius = 8
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 4
ball_dy = -4

# 벽돌 설정
brick_rows = 5
brick_cols = 8
brick_width = WIDTH // brick_cols
brick_height = 30
bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        bricks.append(pygame.Rect(col * brick_width, row * brick_height, brick_width - 2, brick_height - 2))

# 폰트
font = pygame.font.SysFont(None, 50)

# 게임 루프
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    win.fill(BLACK)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    # 공 이동
    ball_x += ball_dx
    ball_y += ball_dy

    # 충돌 처리: 벽
    if ball_x <= 0 or ball_x >= WIDTH:
        ball_dx *= -1
    if ball_y <= 0:
        ball_dy *= -1

    # 충돌 처리: 패들
    paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    if paddle_rect.collidepoint(ball_x, ball_y + ball_radius):
        ball_dy *= -1

    # 충돌 처리: 벽돌
    hit_index = None
    for i, brick in enumerate(bricks):
        if brick.collidepoint(ball_x, ball_y):
            hit_index = i
            break

    if hit_index is not None:
        del bricks[hit_index]
        ball_dy *= -1

    # 공이 바닥으로 떨어짐
    if ball_y >= HEIGHT:
        text = font.render("Game Over", True, RED)
        win.blit(text, (WIDTH//2 - 100, HEIGHT//2 - 25))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    # 승리 조건
    if not bricks:
        text = font.render("You Win!", True, BLUE)
        win.blit(text, (WIDTH//2 - 90, HEIGHT//2 - 25))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    # 그리기
    pygame.draw.circle(win, WHITE, (ball_x, ball_y), ball_radius)
    pygame.draw.rect(win, BLUE, paddle_rect)

    for brick in bricks:
        pygame.draw.rect(win, RED, brick)

    pygame.display.update()

pygame.quit()
sys.exit()