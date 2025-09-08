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

clock = pygame.time.Clock()
font_big   = pygame.font.SysFont(None, 50)
font_small = pygame.font.SysFont(None, 28)

# 패들 설정
paddle_width, paddle_height = 100, 12
paddle_speed = 8

# 공 설정
ball_radius = 8
base_ball_speed = 4  # 스테이지마다 약간 빨라지게 활용

# 벽돌 설정(공통)
BRICK_COLS = 8
BRICK_HEIGHT = 26

def build_bricks(rows, cols=BRICK_COLS, top_offset=50, h=BRICK_HEIGHT, gap=4):
    bricks = []
    brick_width = WIDTH // cols
    for r in range(rows):
        for c in range(cols):
            # 좌우/상하 간격(gap)을 살짝 주어 보기 좋게
            rect = pygame.Rect(
                c * brick_width + gap//2,
                top_offset + r * h + gap//2,
                brick_width - gap,
                h - gap
            )
            bricks.append(rect)
    return bricks

def draw_center_text(text, color, dy=0, big=True):
    surf = (font_big if big else font_small).render(text, True, color)
    win.blit(surf, (WIDTH//2 - surf.get_width()//2, HEIGHT//2 - surf.get_height()//2 + dy))

def reset_positions():
    paddle_x = WIDTH // 2 - paddle_width // 2
    paddle_y = HEIGHT - 30
    ball_x   = WIDTH // 2
    ball_y   = HEIGHT // 2
    return paddle_x, paddle_y, ball_x, ball_y
### 
for row in range(brick_rows):
    for col in range(brick_cols):
        bricks.append(pygame.Rect(col * brick_width, row * brick_height, brick_width - 2, brick_height - 2))

# 폰트
font = pygame.font.SysFont(None, 50)

# 점수
bricks_destroyed = 0
font_small = pygame.font.SysFont(None, 30)

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
        bricks_destroyed += 1   # 점수

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

    # 점수
    score_text = font_small.render(f"Bricks Destroyed: {bricks_destroyed}", True, WHITE)
    win.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
sys.exit()