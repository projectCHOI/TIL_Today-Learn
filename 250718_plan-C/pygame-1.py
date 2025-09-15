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

def draw_arrow(surface, direction, center, size=100, color=(255,255,255)):
    cx, cy = center
    s = size // 2
    if direction == "UP":
        pts = [(cx, cy - s), (cx - s, cy + s), (cx + s, cy + s)]
    elif direction == "DOWN":
        pts = [(cx, cy + s), (cx - s, cy - s), (cx + s, cy - s)]
    elif direction == "LEFT":
        pts = [(cx - s, cy), (cx + s, cy - s), (cx + s, cy + s)]
    elif direction == "RIGHT":
        pts = [(cx + s, cy), (cx - s, cy - s), (cx - s, cy + s)]
    pygame.draw.polygon(surface, color, pts)

def spawn_prompt(prompt_ms):
    choice = random.choice(DIRECTIONS)
    deadline = pygame.time.get_ticks() + prompt_ms
    return choice, deadline

def draw_center_text(surface, text, font, color, y):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH//2, y))
    surface.blit(img, rect)

def game_loop():
    score = 0
    lives = 3
    prompt_ms = 1500        # 시작 제한시간(ms)
    min_prompt_ms = 650     # 최소 제한시간
    decay = 40              # 정답시 제한시간 감소량
    current, deadline = spawn_prompt(prompt_ms)

    running = True

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # 앱 종료
            if event.type == pygame.KEYDOWN:
                # ESC로 즉시 종료
                if event.key == pygame.K_ESCAPE:
                    return False
                # 입력 판정
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    if event.key == current["key"]:
                        # 정답
                        score += 1
                        prompt_ms = max(min_prompt_ms, prompt_ms - decay)
                        current, deadline = spawn_prompt(prompt_ms)
                    else:
                        # 오답
                        lives -= 1
                        if lives <= 0:
                            return game_over_screen(score)
                        current, deadline = spawn_prompt(prompt_ms)

        # 시간 초과 판정
        now = pygame.time.get_ticks()
        if now > deadline:
            lives -= 1
            if lives <= 0:
                return game_over_screen(score)
            current, deadline = spawn_prompt(prompt_ms)

        # 그리기
        win.fill(BLACK)

        # 중앙 방향표시
        draw_center_text(win, current["symbol"], font_big, WHITE, HEIGHT//2)

        # 상단 HUD
        hud = f"Score: {score}   Lives: {lives}   Time: {prompt_ms}ms"
        draw_center_text(win, hud, font_small, GRAY, 24)

        # 타이머 바(남은 시간 비율)
        remain = max(0, deadline - now)
        ratio = remain / prompt_ms
        bar_w = int((WIDTH - 80) * ratio)
        pygame.draw.rect(win, GRAY, (40, HEIGHT - 60, WIDTH - 80, 18), border_radius=6)
        pygame.draw.rect(win, GREEN if ratio > 0.35 else RED, (40, HEIGHT - 60, bar_w, 18), border_radius=6)

        pygame.display.flip()

def game_over_screen(score):
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                # R 재시작
                if event.key == pygame.K_r:
                    return game_loop()
                # ESC 종료
                if event.key == pygame.K_ESCAPE:
                    return False
                
        win.fill(BLACK)
        draw_center_text(win, "GAME OVER", font_mid, RED, HEIGHT//2 - 30)
        draw_center_text(win, f"Final Score: {score}", font_mid, WHITE, HEIGHT//2 + 10)
        draw_center_text(win, "Press R to Restart, ESC to Quit", font_small, GRAY, HEIGHT//2 + 50)
        pygame.display.flip()

if __name__ == "__main__":
    app_running = game_loop()
    pygame.quit()