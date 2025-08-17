# 주사위 돌리기
import pygame
import random
import sys
from pygame.locals import *

# 기본 설정
WIDTH, HEIGHT = 720, 480
FPS = 60

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (30, 30, 30)
GRAY = (200, 200, 200)
PRIMARY = (60, 120, 255)
PRIMARY_DARK = (45, 95, 210)

pygame.init()
pygame.display.set_caption("Dice Six")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 폰트
font_big = pygame.font.SysFont(None, 80)
font_mid = pygame.font.SysFont(None, 32)
font_small = pygame.font.SysFont(None, 24)

# 주사위 속성
DICE_SIZE = 100
DICE_MIN = 1
DICE_MAX = 45
dice_values = [DICE_MIN] * 6
dice_rects = []

# 2행 3열 배치
start_x, start_y = WIDTH // 2 - 180, HEIGHT // 2 - 120
for row in range(2):
    for col in range(3):
        rect = pygame.Rect(0, 0, DICE_SIZE, DICE_SIZE)
        rect.center = (start_x + col * 180, start_y + row * 160)
        dice_rects.append(rect)

# 버튼
button_rect = pygame.Rect(0, 0, 160, 48)
button_rect.center = (WIDTH // 2, HEIGHT - 50)

# 상태
rolling = False
roll_end_time = 0
next_tick_time = 0
roll_step_ms = 80
roll_step_growth = 18

def draw_dice(surface, rect, value, highlight=False):
    body_color = WHITE if not highlight else (245, 250, 255)
    pygame.draw.rect(surface, body_color, rect, border_radius=15)
    pygame.draw.rect(surface, GRAY, rect, width=2, border_radius=15)
    text = font_big.render(str(value), True, DARK)
    surface.blit(text, text.get_rect(center=rect.center))

def draw_button(surface, rect, text, enabled=True, hover=False):
    base = PRIMARY_DARK if hover and enabled else PRIMARY
    if not enabled:
        base = (170, 170, 170)
    pygame.draw.rect(surface, base, rect, border_radius=12)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=12)
    label = font_mid.render(text, True, WHITE if enabled else (230, 230, 230))
    surface.blit(label, label.get_rect(center=rect.center))

def start_roll():
    global rolling, roll_end_time, next_tick_time, roll_step_ms
    if rolling: return
    rolling = True
    now = pygame.time.get_ticks()
    roll_duration_ms = 1200
    roll_step_ms = 50
    roll_end_time = now + roll_duration_ms
    next_tick_time = now + roll_step_ms

def update_roll():
    global rolling, dice_values, dice_rects, next_tick_time, roll_step_ms
    now = pygame.time.get_ticks()
    if now >= roll_end_time:
        rolling = False
        dice_values = [random.randint(1, 6) for _ in range(6)]
        # 위치 원위치
        for i, rect in enumerate(dice_rects):
            row, col = divmod(i, 3)
            rect.center = (WIDTH // 2 - 180 + col * 180, HEIGHT // 2 - 120 + row * 160)
        return

    if now >= next_tick_time:
        dice_values = [random.randint(1, 6) for _ in range(6)]
        for i, rect in enumerate(dice_rects):
            dx, dy = random.randint(-6, 6), random.randint(-6, 6)
            rect.move_ip(dx, dy)
        roll_step_ms += roll_step_growth
        next_tick_time = now + roll_step_ms

def main():
    running = True
    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        hover = button_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if not rolling and button_rect.collidepoint(event.pos):
                    start_roll()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if not rolling:
                    start_roll()

        if rolling:
            update_roll()

        # 그리기
        screen.fill((240, 245, 250))
        title = font_small.render("Press button or SPACE to roll 6 dice", True, (80, 80, 80))
        screen.blit(title, (20, 16))

        for i in range(6):
            draw_dice(screen, dice_rects[i], dice_values[i], highlight=rolling)

        btn_text = "Roll Dice" if not rolling else "Rolling..."
        draw_button(screen, button_rect, btn_text, enabled=not rolling, hover=hover and not rolling)

        # 오름차순 출력
        sorted_vals = sorted(dice_values)
        nums_str = " ".join(str(v) for v in sorted_vals)

        result_text = font_mid.render(f"Sorted: {nums_str}", True, (50, 50, 50))
        screen.blit(result_text, result_text.get_rect(center=(WIDTH // 2, HEIGHT - 100)))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
