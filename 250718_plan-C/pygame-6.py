import pygame
import sys
import math

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame-6")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

# 폰트
FONT_PATH = r"C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\Open Font License\KCC한빛체\KCC한빛체\KCC-Hanbit.ttf"
font = pygame.font.Font(FONT_PATH, 20)
# 플레이어
PLAYER_SIZE = 50
PLAYER_SPEED = 5
player_x = WIDTH // 2
player_y = HEIGHT // 2

# 투사체 설정
PROJECTILE_RADIUS = 6

# 파워 단계 설정
MAX_DRAG = 200
MAX_LEVEL = 10
POWER_TABLE = [0, 0, 8, 10, 12, 14, 16, 18, 20, 22, 25]

# 드래그 상태
dragging = False
press_pos = (0, 0)
current_pos = (0, 0)

projectiles = []

clock = pygame.time.Clock()
running = True

class Projectile:
    def __init__(self, pos, velocity):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(velocity)

    def update(self):
        self.pos += self.vel
        self.vel *= 0.99  # 간단한 감속

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, self.pos, PROJECTILE_RADIUS)

while running: