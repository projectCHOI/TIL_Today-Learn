import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 640, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer - Improved")

WHITE=(255,255,255); BLUE=(0,120,255); GREEN=(40,180,60); BLACK=(0,0,0)

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
        
pygame.quit()
sys.exit()