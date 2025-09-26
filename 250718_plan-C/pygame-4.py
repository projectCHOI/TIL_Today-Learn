import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 800, 300
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Dino (Obstacles)")
clock = pygame.time.Clock()

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (220, 40, 40)
GREEN = (40, 200, 60)
GRAY  = (120, 120, 120)

# 지면 설정
GROUND_Y = 240
SCROLL_SPEED_BASE = 260.0  # px/s (장식용)
world_speed = 380.0        # 장애물 이동 속도 (px/s)
speed_growth = 0.04        # 초당 속도 증가량

# Dino
DINO_WIDTH, DINO_HEIGHT = 44, 50
DINO_DUCK_HEIGHT = 32
dino_x = 80
dino_y = GROUND_Y - DINO_HEIGHT
dino_vel_y = 0.0

GRAVITY = 2000.0     # px/s^2
JUMP_POWER = -650.0  # px/s
on_ground = True
is_ducking = False

ground_offset = 0.0

def get_dino_rect():
    h = DINO_DUCK_HEIGHT if is_ducking else DINO_HEIGHT
    y = GROUND_Y - h if on_ground else (dino_y + (DINO_HEIGHT - h))
    return pygame.Rect(int(dino_x), int(y), DINO_WIDTH, h)

# --- 장애물 공통 설정 ---
class Obstacle:
    def __init__(self, kind, x, speed):
        self.kind = kind
        self.speed = speed
        if kind == "cactus_small":
            self.w, self.h = 22, 40
            self.y = GROUND_Y - self.h
        elif kind == "cactus_tall":
            self.w, self.h = 28, 60
            self.y = GROUND_Y - self.h
        elif kind == "bird_low":
            self.w, self.h = 46, 30
            # 숙이기(32px)로 피하도록 낮은 높이
            self.y = GROUND_Y - DINO_DUCK_HEIGHT - self.h - 4
        elif kind == "bird_high":
            self.w, self.h = 46, 30
            # 그냥 지나가거나 점프 타이밍 교란
            self.y = GROUND_Y - DINO_HEIGHT - self.h - 12
        else:
            self.w, self.h = 20, 40
            self.y = GROUND_Y - self.h

        self.x = x

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, dt, speed):
        self.x -= speed * dt

    def draw(self, surf):
        color = BLACK if "cactus" in self.kind else GRAY
        pygame.draw.rect(surf, color, self.rect)

# 스폰 관리
obstacles = []
time_to_next_spawn = 0  # ms
min_spawn_ms = 800
max_spawn_ms = 1600

# 점수/상태
score = 0
best_score = 0
game_over = False

def schedule_next_spawn():
    global time_to_next_spawn
    time_to_next_spawn = random.randint(min_spawn_ms, max_spawn_ms)
    
class Cactus:
    def __init__(self):
        self.w = random.choice([28, 34, 44])    # 장애물 폭 가변
        self.h = random.choice([46, 60, 72])    # 장애물 높이 가변
        self.x = WIDTH + 10
        self.y = GROUND_Y - self.h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self, speed):
        self.x -= speed
        self.rect.x = int(self.x)

    def draw(self, surf):
        pygame.draw.rect(surf, (34, 139, 34), self.rect)  # 초록

    @property
    def offscreen(self):
        return self.rect.right < -20
    
running = True

while running:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # 점프
    if keys[pygame.K_UP] and on_ground:
        dino_vel_y = JUMP_POWER
        on_ground = False

    # 숙이기: 아래 화살표 유지 시
    is_ducking = keys[pygame.K_DOWN] and on_ground

    # 수직(중력/점프)
    if not on_ground:
        dino_vel_y += GRAVITY * dt
        dino_y += dino_vel_y * dt

        # 바닥 충돌
        if dino_y >= GROUND_Y - DINO_HEIGHT:
            dino_y = GROUND_Y - DINO_HEIGHT
            dino_vel_y = 0
            on_ground = True

    # 배경 지면 라인 스크롤(장식)
    ground_offset = (ground_offset - SCROLL_SPEED) % 40

    win.fill(WHITE)

    # 지면
    pygame.draw.line(win, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
    # 지면에 작은 틱 표시(스크롤 느낌)
    for x in range(-40, WIDTH + 40, 40):
        pygame.draw.line(win, GREEN, (x + ground_offset, GROUND_Y), (x + 10 + ground_offset, GROUND_Y), 2)

    # Dino캐릭터
    dino_rect = get_dino_rect()
    pygame.draw.rect(win, RED, dino_rect)

    # 안내 텍스트
    FONT_PATH = r"C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\Open Font License\서평원 꺾깎체\TTF\SLEIGothicTTF.ttf"
    font = pygame.font.Font(FONT_PATH, 20)
    text = font.render("↑ jump, ↓ duck (ESC to quit)", True, BLACK)
    win.blit(text, (10, 10))

    pygame.display.flip()

    # ESC로 종료
    if keys[pygame.K_ESCAPE]:
        running = False
        
pygame.quit()
sys.exit()