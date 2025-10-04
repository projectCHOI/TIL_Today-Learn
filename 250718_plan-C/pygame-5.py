import pygame
import math

# 초기 설정
pygame.init()
WIDTH, HEIGHT = 640, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("숫자 범위 선택 게임 - 베이스")

# 색상
WHITE = (255, 255, 255)
YELLOW = (255, 244, 79)
BLUE   = (0, 120, 255)

FPS = 60
CLOCK = pygame.time.Clock()

# 유닛
def create_star_surface(size, color):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size / 2, size / 2
    R = size * 0.48       # 바깥 반지름
    r = R * 0.5           # 안쪽 반지름
    points = []
    # 꼭대기가 위를 향하도록 -90도(= -pi/2)에서 시작
    start_angle = -math.pi / 2
    for i in range(10):
        ang = start_angle + i * (math.pi / 5)  # 36도 간격
        radius = R if i % 2 == 0 else r
        x = cx + radius * math.cos(ang)
        y = cy + radius * math.sin(ang)
        points.append((x, y))
    pygame.draw.polygon(surf, color, points)
    return surf