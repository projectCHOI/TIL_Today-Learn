import pygame
import random

pygame.init()
WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arrow Prompt Game")

# 색상
BLACK = (0,0,0); WHITE=(255,255,255); GREEN=(0,255,0); RED=(255,60,60); GRAY=(120,120,120); YELLOW=(255,255,0)

# 폰트
font_big  = pygame.font.SysFont(None, 80) # 크기 조정
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
