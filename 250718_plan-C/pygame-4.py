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

def spawn_obstacle():
    x = WIDTH + 30
    # 간단한 가중치
    kinds = (
        ["cactus_small"] * 4 +
        ["cactus_tall"]  * 3 +
        ["bird_low"]     * 2 +
        ["bird_high"]    * 1
    )
    kind = random.choice(kinds)
    obstacles.append(Obstacle(kind, x, world_speed))

def reset_game():
    global dino_y, dino_vel_y, on_ground, is_ducking
    global obstacles, score, game_over, world_speed, ground_offset
    dino_y = GROUND_Y - DINO_HEIGHT
    dino_vel_y = 0.0
    on_ground = True
    is_ducking = False
    obstacles = []
    score = 0
    game_over = False
    world_speed = 380.0
    ground_offset = 0.0
    schedule_next_spawn()

# 초기 스폰 예약
schedule_next_spawn()

running = True
while running:
    dt = clock.tick(60) / 1000.0  # 초 단위 dt

    # 이벤트
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # 입력
        if keys[pygame.K_UP] and on_ground:
            dino_vel_y = JUMP_POWER
            on_ground = False
        is_ducking = keys[pygame.K_DOWN] and on_ground

        # 물리
        if not on_ground:
            dino_vel_y += GRAVITY * dt
            dino_y += dino_vel_y * dt
            if dino_y >= GROUND_Y - DINO_HEIGHT:
                dino_y = GROUND_Y - DINO_HEIGHT
                dino_vel_y = 0.0
                on_ground = True

        # 난이도 증가
        world_speed += speed_growth

        # 장애물 스폰 타이머(ms)
        time_to_next_spawn -= int(dt * 1000)
        if time_to_next_spawn <= 0:
            # 연속 피하기가 가능하도록, 바로 앞 장애물과 최소 간격 보정
            if not obstacles or (obstacles and obstacles[-1].x < WIDTH - 160):
                spawn_obstacle()
                schedule_next_spawn()
            else:
                # 간격이 너무 좁으면 조금 뒤로 미룸
                time_to_next_spawn = 150

        # 장애물 업데이트/정리
        for ob in obstacles:
            ob.update(dt, world_speed)
        obstacles = [ob for ob in obstacles if ob.x + ob.w > -30]

        # 점수 (생존 시간 기반)
        score += int(60 * dt)

        # 충돌 판정
        dino_rect = get_dino_rect()
        for ob in obstacles:
            if dino_rect.colliderect(ob.rect):
                game_over = True
                break

        # 지면 장식 스크롤
        ground_offset = (ground_offset - SCROLL_SPEED_BASE * dt) % 40

    else:
        # 재시작
        if keys[pygame.K_r]:
            best_score = max(best_score, score)
            reset_game()

    win.fill(WHITE)
    # 지면
    pygame.draw.line(win, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
    x = -40
    while x < WIDTH + 40:
        pygame.draw.line(win, GREEN, (int(x + ground_offset), GROUND_Y),
                        (int(x + 10 + ground_offset), GROUND_Y), 2)
        x += 40

    # Dino
    pygame.draw.rect(win, RED, get_dino_rect())

    # 장애물
    for ob in obstacles:
        ob.draw(win)  

    # UI
    if not game_over:
        ui = f"↑ jump, ↓ duck | Score: {score} | Speed: {int(world_speed)} (R: reset)"
    else:
        ui = f"GAME OVER  Score: {score}  Best: {best_score}  (Press R to restart)"

    win.blit(text, (10, 10))

    pygame.display.flip()

    # 글꼴 불러오기 (크기 22px)
    FONT_PATH = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/Open Font License/서평원 꺾깎체/TTF/SLEIGothicTTF.ttf"
    font = pygame.font.Font(FONT_PATH, 22)
    
    if keys[pygame.K_ESCAPE]:
        running = False

pygame.quit()
sys.exit()