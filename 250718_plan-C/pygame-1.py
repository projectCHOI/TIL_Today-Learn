import pygame
import random
import os

pygame.init()
WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("순발력 화살표 게임")

# 색상
BLACK = (0,0,0); WHITE=(255,255,255); GREEN=(0,255,0); RED=(255,60,60); GRAY=(120,120,120); YELLOW=(255,255,0)
FONT_PATH = r"C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\Open Font License\서평원 꺾깎체\TTF\SLEIGothicTTF.ttf"

if os.path.exists(FONT_PATH):
    font_big   = pygame.font.Font(FONT_PATH, 80)
    font_mid   = pygame.font.Font(FONT_PATH, 36)
    font_small = pygame.font.Font(FONT_PATH, 20)
else:
    print("폰트 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    font_big   = pygame.font.SysFont("malgungothic", 80)
    font_mid   = pygame.font.SysFont("malgungothic", 36)
    font_small = pygame.font.SysFont("malgungothic", 20)

clock = pygame.time.Clock()
FPS = 60

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

DIRECTIONS = [
    {"name":"UP",    "key":pygame.K_UP},
    {"name":"DOWN",  "key":pygame.K_DOWN},
    {"name":"LEFT",  "key":pygame.K_LEFT},
    {"name":"RIGHT", "key":pygame.K_RIGHT},
]

def start_screen():
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return game_loop()
                if event.key == pygame.K_ESCAPE:
                    return False

        win.fill(BLACK)
        draw_center_text(win, "순발력 테스트", font_big, GREEN, HEIGHT//2 - 100)
        
        draw_center_text(win, "[ 게임 방법 ]", font_mid, WHITE, HEIGHT//2 - 10)
        draw_center_text(win, "화살표 방향키를 정확하게 누르세요!", font_small, GRAY, HEIGHT//2 + 30)
        draw_center_text(win, "틀리거나 시간이 초과되면 생명이 깎입니다.", font_small, GRAY, HEIGHT//2 + 55)
        
        draw_center_text(win, "엔터(Enter)를 눌러 시작", font_mid, YELLOW, HEIGHT//2 + 130)
        draw_center_text(win, "ESC를 눌러 종료", font_small, GRAY, HEIGHT//2 + 170)
        
        pygame.display.flip()

def game_loop():
    score = 0
    lives = 3
    prompt_ms = 1500
    min_prompt_ms = 650
    decay = 40
    current, deadline = spawn_prompt(prompt_ms)

    while True:
        clock.tick(FPS)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return start_screen()
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    if event.key == current["key"]:
                        score += 1
                        prompt_ms = max(min_prompt_ms, prompt_ms - decay)
                        current, deadline = spawn_prompt(prompt_ms)
                    else:
                        lives -= 1
                        if lives <= 0: return game_over_screen(score)
                        current, deadline = spawn_prompt(prompt_ms)

        if now > deadline:
            lives -= 1
            if lives <= 0: return game_over_screen(score)
            current, deadline = spawn_prompt(prompt_ms)

        win.fill(BLACK)
        draw_arrow(win, current["name"], (WIDTH//2, HEIGHT//2), size=160, color=WHITE)
        
        # HUD 한글 적용
        hud = f"점수: {score}   목숨: {lives}   속도: {prompt_ms}ms"
        draw_center_text(win, hud, font_small, GRAY, 24)

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
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return game_loop()
                if event.key == pygame.K_m: return start_screen()
                if event.key == pygame.K_ESCAPE: return False
                
        win.fill(BLACK)
        draw_center_text(win, "게임 오버", font_mid, RED, HEIGHT//2 - 30)
        draw_center_text(win, f"최종 점수: {score}", font_mid, WHITE, HEIGHT//2 + 10)
        draw_center_text(win, "R: 재시작  M: 메뉴로  ESC: 종료", font_small, GRAY, HEIGHT//2 + 60)
        pygame.display.flip()

if __name__ == "__main__":
    start_screen()
    pygame.quit()