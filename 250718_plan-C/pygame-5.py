import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 640, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer - Improved")

WHITE=(255,255,255); BLUE=(0,120,255); GREEN=(40,180,60); BLACK=(0,0,0)
RED = (255, 0, 0)

GRAVITY = 2000     # px/s^2
MOVE_ACC = 4000    # 좌우 가속
FRICTION = 0.85    # 지상 감속 계수
MAX_SPEED_X = 300
MAX_FALL = 900
JUMP_VEL = -600
COYOTE_TIME = 0.10     # 초
JUMP_BUFFER = 0.10     # 초
JUMP_CUT = 0.5         # 점프 중 키를 떼면 상승속도 절반으로 컷

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

class Platform:
    def __init__(self, x, y, w, h, vx=0, range_px=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.vx = vx
        self.range_px = range_px
        self.origin_x = x
        self.dir = 1

    def update(self, dt):
        if self.vx == 0: return
        self.rect.x += self.dir * int(self.vx * dt)
        if abs(self.rect.x - self.origin_x) >= self.range_px:
            self.dir *= -1

    def draw(self, surf):
        pygame.draw.rect(surf, GREEN, self.rect)

class Player:
    def __init__(self, x, y, w=40, h=50):
        self.rect = pygame.Rect(x, y, w, h)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.coyote = 0.0
        self.jump_buf = 0.0
        self.want_jump = False

    def handle_input(self, keys):
        ax = 0.0
        if keys[pygame.K_LEFT]: ax -= MOVE_ACC
        if keys[pygame.K_RIGHT]: ax += MOVE_ACC
        return ax

    def try_jump(self):
        # 점프 조건: 지상 or 코요테 타임, 그리고 점프 버퍼 안에 입력 존재
        if (self.on_ground or self.coyote > 0.0) and self.jump_buf > 0.0:
            self.vy = JUMP_VEL
            self.on_ground = False
            self.coyote = 0.0
            self.jump_buf = 0.0

    def update(self, dt, platforms, keys):
        # 입력
        ax = self.handle_input(keys)

        # 수평 속도 업데이트 (가속 + 마찰)
        self.vx += ax * dt
        if self.on_ground and ax == 0:
            self.vx *= FRICTION
        # 속도 클램프
        self.vx = max(-MAX_SPEED_X, min(MAX_SPEED_X, self.vx))

        # 중력
        self.vy += GRAVITY * dt
        self.vy = min(self.vy, MAX_FALL)

        # 코요테/버퍼 타이머 감소
        if not self.on_ground:
            self.coyote -= dt
        self.jump_buf -= dt

        # 점프 시도(버퍼·코요테 반영)
        self.try_jump()

        # === 충돌: 수평 이동 먼저 ===
        dx = int(self.vx * dt)
        self.rect.x += dx
        hit_plat = None
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if dx > 0:
                    self.rect.right = p.rect.left
                elif dx < 0:
                    self.rect.left = p.rect.right

        # === 충돌: 수직 이동 ===
        dy = int(self.vy * dt)
        self.rect.y += dy
        self.on_ground = False
        landed_on = None
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if dy > 0:  # 아래로 떨어지는 중 → 착지
                    self.rect.bottom = p.rect.top
                    self.vy = 0
                    self.on_ground = True
                    landed_on = p
                    self.coyote = COYOTE_TIME
                elif dy < 0:  # 위로 상승 중 → 머리 부딪힘
                    self.rect.top = p.rect.bottom
                    self.vy = 0

        # 이동 발판 위에 있으면 발판 이동분만큼 같이 밀어주기
        if self.on_ground and landed_on and landed_on.vx != 0:
            self.rect.x += landed_on.dir * int(landed_on.vx * dt)

        # 화면 경계
        if self.rect.left < 0: self.rect.left = 0; self.vx = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH; self.vx = 0
        if self.rect.top > HEIGHT + 200:  # 떨어지면 리셋
            self.rect.topleft = (100, HEIGHT - 120)
            self.vx = self.vy = 0
            self.on_ground = False
            self.coyote = 0
            self.jump_buf = 0

        # 가변 점프: 키에서 손 떼면 상승 속도 컷
        if not keys[pygame.K_SPACE] and self.vy < 0:
            self.vy *= JUMP_CUT

    def queue_jump(self):
        self.jump_buf = JUMP_BUFFER

    def draw(self, surf):
        pygame.draw.rect(surf, BLUE, self.rect)

# 레벨 구성
platforms = [
    Platform(0, HEIGHT-30, WIDTH, 30),               # 바닥
    Platform(120, 300, 120, 18),
    Platform(300, 240, 120, 18),
    Platform(480, 180, 100, 18),
    Platform(180, 150, 90, 18, vx=80, range_px=120), # 좌우로 움직이는 발판
]

player = Player(100, HEIGHT - 120)

goal_radius = max(8, int(player.rect.w * 0.5 * 0.5))  # 원 크기
goal_pos = [WIDTH - 60, 120]  # 원하는 위치
game_clear = False             # 게임 클리어 상태

def rect_circle_collide(rect, cx, cy, r):
    nearest_x = max(rect.left, min(cx, rect.right))
    nearest_y = max(rect.top,  min(cy, rect.bottom))
    dx = cx - nearest_x
    dy = cy - nearest_y
    return (dx*dx + dy*dy) <= r*r

def draw_hud():
    text = font.render("←/→ Move, SPACE Jump | R: Reset | ESC: Quit", True, BLACK)
    win.blit(text, (10, 10))

running = True
while running:
    dt = clock.tick(60) / 1000.0  # 초 단위
    for e in pygame.event.get():
        if e.type == pygame.QUIT: running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE: running = False
            if e.key == pygame.K_r:
                player.rect.topleft = (100, HEIGHT-120)
                player.vx = player.vy = 0
                player.on_ground = False
                player.coyote = 0
                player.jump_buf = 0
                game_clear = False   # [NEW] 클리어 상태 초기화
            if e.key == pygame.K_SPACE and not game_clear:
                player.queue_jump()

    keys = pygame.key.get_pressed()

if not game_clear:
    # 타겟 원 그리기
    pygame.draw.circle(win, RED, goal_pos, goal_radius)

    # 플랫폼 그리기
    for p in platforms:
        p.draw(win)
    player.draw(win)

    # 플랫폼 업데이트
    for p in platforms:
        p.update(dt)

    # 플레이어 업데이트
    player.update(dt, platforms, keys)

    # [NEW] 목표물 충돌 체크
    if rect_circle_collide(player.rect, goal_pos[0], goal_pos[1], goal_radius):
        game_clear = True

    # 렌더
    win.fill(WHITE)
    for p in platforms: p.draw(win)
    player.draw(win)
    draw_hud()
    pygame.display.flip()
    
pygame.quit()
sys.exit()


# (2) 업데이트 부분