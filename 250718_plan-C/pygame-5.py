import pygame

# === 초기 설정 ===
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