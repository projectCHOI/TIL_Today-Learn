import pygame
pygame.init()

# 창 설정
WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Box - Improved")

# 색상
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# 사각형 설정
x, y = WIDTH // 2, HEIGHT // 2
width, height = 40, 40
vel = 5

# 점수 관련
score = 0
font = pygame.font.SysFont("comicsans", 30)
last_score_update = pygame.time.get_ticks()

# 시계 설정
clock = pygame.time.Clock()
FPS = 60

run = True
while run:
    clock.tick(FPS)  # 프레임 제한

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x = max(0, x - vel)
    if keys[pygame.K_RIGHT]:
        x = min(WIDTH - width, x + vel)
    if keys[pygame.K_UP]:
        y = max(0, y - vel)
    if keys[pygame.K_DOWN]:
        y = min(HEIGHT - height, y + vel)

    # 점수 증가 (0.5초마다 1점 증가)
    current_time = pygame.time.get_ticks()
    if current_time - last_score_update > 500:  # 500ms
        score += 1
        last_score_update = current_time

    # 화면 그리기
    win.fill(BLACK)
    pygame.draw.rect(win, GREEN, (x, y, width, height))

    score_text = font.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
