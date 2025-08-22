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
        if (self.on_ground or self.coyote > 0.0) and self.jump_buf > 0.0:
            self.vy = JUMP_VEL
            self.on_ground = False
            self.coyote = 0.0
            self.jump_buf = 0.0

    def update(self, dt, platforms, keys):
        ax = self.handle_input(keys)

        # 수평 속도
        self.vx += ax * dt
        if self.on_ground and ax == 0:
            self.vx *= FRICTION
        self.vx = max(-MAX_SPEED_X, min(MAX_SPEED_X, self.vx))

        # 중력
        self.vy += GRAVITY * dt
        self.vy = min(self.vy, MAX_FALL)

        # 타이머
        if not self.on_ground:
            self.coyote -= dt
        self.jump_buf -= dt

        # 점프 시도
        self.try_jump()

        # === 충돌: 수평 ===
        dx = int(self.vx * dt)
        self.rect.x += dx
        landed_on = None
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if dx > 0:
                    self.rect.right = p.rect.left
                elif dx < 0:
                    self.rect.left = p.rect.right

        # === 충돌: 수직 ===
        dy = int(self.vy * dt)
        self.rect.y += dy
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if dy > 0:
                    self.rect.bottom = p.rect.top
                    self.vy = 0
                    self.on_ground = True
                    landed_on = p
                    self.coyote = COYOTE_TIME
                elif dy < 0:
                    self.rect.top = p.rect.bottom
                    self.vy = 0

        # 이동 발판 동승
        if self.on_ground and landed_on and landed_on.vx != 0:
            self.rect.x += landed_on.dir * int(landed_on.vx * dt)

        # 화면 경계 / 떨어짐 리셋
        if self.rect.left < 0:
            self.rect.left = 0; self.vx = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH; self.vx = 0
        if self.rect.top > HEIGHT + 200:
            self.rect.topleft = (100, HEIGHT - 120)
            self.vx = self.vy = 0
            self.on_ground = False
            self.coyote = 0
            self.jump_buf = 0

        # 가변 점프
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
    Platform(180, 150, 90, 18, vx=80, range_px=120), # 좌우 이동 발판
]

player = Player(100, HEIGHT - 120)

# === 목표물(원) 설정 ===
target_platform = 2   # 0=바닥, 1=첫 번째, 2=두 번째, ...
plat = platforms[target_platform]

goal_radius = max(8, int(player.rect.w * 0.5 * 0.5))
goal_pos = [plat.rect.centerx, plat.rect.top - goal_radius]
game_clear = False

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
    dt = clock.tick(60) / 1000.0

    # 입력/이벤트
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False
            if e.key == pygame.K_r:
                # 리셋 시 클리어 상태도 초기화
                player.rect.topleft = (100, HEIGHT-120)
                player.vx = player.vy = 0
                player.on_ground = False
                player.coyote = 0
                player.jump_buf = 0
                game_clear = False
            if e.key == pygame.K_SPACE and not game_clear:
                player.queue_jump()

    keys = pygame.key.get_pressed()

    # === 업데이트 ===
    if not game_clear:
        plat = platforms[target_platform]
        goal_pos = [plat.rect.centerx, plat.rect.top - goal_radius]

        for p in platforms:
            p.update(dt)
        player.update(dt, platforms, keys)

        # 충돌 판정
        if rect_circle_collide(player.rect, goal_pos[0], goal_pos[1], goal_radius):
            game_clear = True

    # === 렌더 ===
    win.fill(WHITE)

    # 목표 원 (클리어 전까지 표시)
    if not game_clear:
        pygame.draw.circle(win, RED, goal_pos, goal_radius)

    # 플랫폼/플레이어 표시는 상태와 무관하게 그려도 좋음(정지된 장면 보여주기)
    for p in platforms:
        p.draw(win)
    player.draw(win)

    draw_hud()

    # 클리어 메시지
    if game_clear:
        msg = font.render("🎉 STAGE CLEAR! (R: Reset, ESC: Quit)", True, BLACK)
        win.blit(msg, (WIDTH//2 - msg.get_width()//2, 40))

    pygame.display.flip()

pygame.quit()
sys.exit()
