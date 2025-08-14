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
pygame.display.set_caption("Dice Numbus")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 폰트
font_big = pygame.font.SysFont(None, 100)
font_mid = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)

# 주사위 속성
DICE_SIZE = 140
# 첫 번째 주사위
dice1_rect = pygame.Rect(0, 0, DICE_SIZE, DICE_SIZE)
dice1_rect.center = (WIDTH // 2 - 100, HEIGHT // 2 - 30)
# 두 번째 주사위
dice2_rect = pygame.Rect(0, 0, DICE_SIZE, DICE_SIZE)
dice2_rect.center = (WIDTH // 2 + 100, HEIGHT // 2 - 30)

# 버튼
button_rect = pygame.Rect(0, 0, 160, 48)
button_rect.center = (WIDTH // 2, HEIGHT - 60)

# 상태
current_value = 1
rolling = False
roll_end_time = 0
next_tick_time = 0
roll_step_ms = 80          # 시작 틱 간격
roll_step_growth = 18      # 틱 간격 증가량(감속 효과)

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

    # 버튼 렌더링
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
    if rolling:
        return
    rolling = True
    now = pygame.time.get_ticks()
    roll_duration_ms = 900     # 전체 굴리는 시간
    roll_step_ms = 50          # 시작은 빠르게
    roll_end_time = now + roll_duration_ms
    next_tick_time = now + roll_step_ms

    # 굴리는 동안 숫자/위치 업데이트 (감속 애니메이션)
def update_roll():
    global rolling, current_value, dice_rect, next_tick_time, roll_end_time, roll_step_ms
    now = pygame.time.get_ticks()

    if now >= roll_end_time:
        rolling = False
        current_value = random.randint(1, 6)  # 최종 값
        dice_rect.center = (WIDTH // 2, HEIGHT // 2 - 30)  # 중앙 복귀
        return

    # 틱마다 숫자/위치 갱신 (작게 흔들리는 효과)
    if now >= next_tick_time:
        current_value = random.randint(1, 6)
        dx = random.randint(-8, 8)
        dy = random.randint(-8, 8)
        dice_rect.center = (WIDTH // 2 + dx, HEIGHT // 2 - 30 + dy)
        # 다음 틱을 더 느리게 해서 감속처럼 보이게
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
            elif event.type == KEYDOWN:
                # 스페이스바로도 굴리기 시작
                if event.key == K_SPACE and not rolling:
                    start_roll()

        if rolling:
            update_roll()

        # 그리기
        screen.fill((245, 246, 250))
        title = font_small.render("press the button", True, (80, 80, 80))
        screen.blit(title, (20, 16))

        draw_dice(screen, dice_rect, current_value, highlight=rolling)

        btn_text = "Button" if not rolling else "wooooo..."
        draw_button(screen, button_rect, btn_text, enabled=not rolling, hover=hover and not rolling)

        # 결과 안내 (앞의 작은 따옴표 제거)
        result_text = font_mid.render(f"No.: {current_value}", True, (50, 50, 50))
        screen.blit(result_text, result_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120)))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()