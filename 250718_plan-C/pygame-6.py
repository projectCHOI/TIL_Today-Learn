import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame-6: Target System")

# 색상 변경
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)  # 플레이어 색상
RED = (255, 0, 0)    # 적 색상
GRAY = (200, 200, 200)
DARK_BLUE = (0, 50, 150) # 패널티 상태 플레이어

# 폰트 설정
try:
    FONT_PATH = r"C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\Open Font License\KCC한빛체\KCC한빛체\KCC-Hanbit.ttf"
    font = pygame.font.Font(FONT_PATH, 20)
except:
    font = pygame.font.SysFont("arial", 20)

# 플레이어 설정
PLAYER_SIZE = 50
PLAYER_SPEED = 5
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

# 적(Target) 설정
ENEMY_SIZE = 50
ENEMY_SPEED = 3
enemy_pos = pygame.Vector2(100, 100)
enemy_move_timer = pygame.time.get_ticks()
enemy_is_moving = True

# 투사체 설정
PROJECTILE_RADIUS = 6
MAX_DRAG = 200
MAX_LEVEL = 10
POWER_TABLE = [0, 0, 8, 10, 12, 14, 16, 18, 20, 22, 25]

# 상태 변수
dragging = False
press_pos = pygame.Vector2(0, 0)
projectiles = []
can_move = True

class Projectile:
    def __init__(self, pos, velocity):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(velocity)

    def update(self):
        self.pos += self.vel
        self.vel *= 0.99 

    def draw(self, screen):
        # 투사체 색상은 플레이어와 맞춤
        pygame.draw.circle(screen, BLUE, self.pos, PROJECTILE_RADIUS)

clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks()
    current_level = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            press_pos = pygame.Vector2(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
            release_pos = pygame.Vector2(pygame.mouse.get_pos())
            drag_vec = release_pos - press_pos

        if drag_vec.length() > 0:
                        if drag_vec.length() > MAX_DRAG:
                            drag_vec = drag_vec.normalize() * MAX_DRAG

                        level = int(drag_vec.length() / (MAX_DRAG / MAX_LEVEL))
                        level = max(0, min(level, MAX_LEVEL))

                        if level >= 2:
                            direction = -drag_vec.normalize()
                            speed = POWER_TABLE[level]
                            velocity = direction * speed
                            projectiles.append(
                                Projectile(player_pos + pygame.Vector2(PLAYER_SIZE // 2, PLAYER_SIZE // 2), velocity)
                            )

    can_move = True
    if dragging:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        drag_vec = mouse_pos - press_pos
        current_dist = min(drag_vec.length(), MAX_DRAG)
        current_level = int(current_dist / (MAX_DRAG / MAX_LEVEL))
        if current_level >= 10:
            can_move = False