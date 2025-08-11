# 주사위 돌리기
import pygame
import random
import sys
from pygame.locals import *

# 기본 설정
WIDTH, HEIGHT = 520, 420
FPS = 60

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (30, 30, 30)
GRAY = (200, 200, 200)
PRIMARY = (60, 120, 255)
PRIMARY_DARK = (45, 95, 210)
GREEN = (40, 160, 80)

pygame.init()
pygame.display.set_caption("주사위 굴리기 - Pygame Basic")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 폰트
font_big = pygame.font.SysFont(None, 100)
font_mid = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)

# 주사위 속성
DICE_SIZE = 140
dice_rect = pygame.Rect(0, 0, DICE_SIZE, DICE_SIZE)
dice_rect.center = (WIDTH // 2, HEIGHT // 2 - 30)

# 버튼
button_rect = pygame.Rect(0, 0, 160, 48)
button_rect.center = (WIDTH // 2, HEIGHT - 60)

# 상태
current_value = 1
rolling = False
roll_end_time = 0
next_tick_time = 0

def draw_dice(surface, rect, value, highlight=False):
    """숫자 주사위를 그립니다(둥근 모서리 + 숫자)."""
    # 본체
    body_color = WHITE if not highlight else (245, 250, 255)
    pygame.draw.rect(surface, body_color, rect, border_radius=18)
    pygame.draw.rect(surface, GRAY, rect, width=2, border_radius=18)

    # 숫자
    text = font_big.render(str(value), True, DARK)
    text_rect = text.get_rect(center=rect.center)
    surface.blit(text, text_rect)

def draw_button(surface, rect, text, enabled=True, hover=False):
    """버튼 렌더링"""
    base = PRIMARY_DARK if hover and enabled else PRIMARY
    if not enabled:
        base = (170, 170, 170)
    pygame.draw.rect(surface, base, rect, border_radius=12)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=12)
    label = font_mid.render(text, True, WHITE if enabled else (230, 230, 230))
    surface.blit(label, label.get_rect(center=rect.center))
    
pygame.quit()
sys.exit()

if __name__ == "__main__":
    main()