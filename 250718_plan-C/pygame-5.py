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

# 플레이어
class Player:
    def __init__(self, x, y, size=50, speed=4):
        self.size = size
        self.speed = speed
        self.base_color = YELLOW
        self.select_color = BLUE
        # 기본/선택 상태 별 Surface
        self.surf_base = create_star_surface(self.size, self.base_color)
        self.surf_select = create_star_surface(self.size, self.select_color)
        # 위치는 중심 좌표로 관리
        self.x = x
        self.y = y
        # 회전 애니메이션 상태
        self.rotating = False
        self.angle = 0
        self.rotate_ms = 400  # 애니메이션 총 길이(ms)
        self.rotate_start_time = 0