import pygame
import random

pygame.init()
WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arrow Prompt Game")

# 색상
BLACK = (0,0,0); WHITE=(255,255,255); GREEN=(0,255,0); RED=(255,60,60); GRAY=(120,120,120); YELLOW=(255,255,0)

# 폰트
font_big  = pygame.font.SysFont(None, 80)
font_mid  = pygame.font.SysFont(None, 36)
font_small= pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()
FPS = 60

# 방향 정의
DIRECTIONS = [
    {"name":"UP",    "key":pygame.K_UP},
    {"name":"DOWN",  "key":pygame.K_DOWN},
    {"name":"LEFT",  "key":pygame.K_LEFT},
    {"name":"RIGHT", "key":pygame.K_RIGHT},
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

# --- 신규 추가: 시작 화면 ---
def start_screen():
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # 엔터키 입력 시 게임 시작
                    return game_loop()
                if event.key == pygame.K_ESCAPE:
                    return False

        win.fill(BLACK)
        # 배경 및 제목
        draw_center_text(win, "ARROW PROMPT", font_big, GREEN, HEIGHT//2 - 100)
        
        # 게임 방법 안내
        draw_center_text(win, "[ 게임 방법 ]", font_mid, WHITE, HEIGHT//2 - 10)
        draw_center_text(win, "화면에 나오는 화살표 방향키를 누르세요!", font_small, GRAY, HEIGHT//2 + 30)
        draw_center_text(win, "시간이 다 되거나 틀리면 생명이 깎입니다.", font_small, GRAY, HEIGHT//2 + 55)
        
        # 시작 안내 (깜빡이는 효과를 주면 더 좋습니다)
        draw_center_text(win, "Press ENTER to Start", font_mid, YELLOW, HEIGHT//2 + 130)
        draw_center_text(win, "Press ESC to Quit", font_small, GRAY, HEIGHT//2 + 170)
        
        pygame.display.flip()
