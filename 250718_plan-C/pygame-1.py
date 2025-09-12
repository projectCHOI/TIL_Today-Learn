import pygame
import random

pygame.init()
WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arrow Prompt Game")

# 색상
BLACK = (0,0,0); WHITE=(255,255,255); GREEN=(0,255,0); RED=(255,60,60); GRAY=(120,120,120)

# 폰트
font_big  = pygame.font.SysFont(None, 140)
font_mid  = pygame.font.SysFont(None, 36)
font_small= pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()
FPS = 60

# 방향 정의
DIRECTIONS = [
    {"name":"UP",    "key":pygame.K_UP,    "symbol":"▲"},
    {"name":"DOWN",  "key":pygame.K_DOWN,  "symbol":"▼"},
    {"name":"LEFT",  "key":pygame.K_LEFT,  "symbol":"◀"},
    {"name":"RIGHT", "key":pygame.K_RIGHT, "symbol":"▶"},
]

def spawn_prompt(prompt_ms):
    choice = random.choice(DIRECTIONS)
    deadline = pygame.time.get_ticks() + prompt_ms
    return choice, deadline

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
