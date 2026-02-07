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
