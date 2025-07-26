import pygame
import sys

# 초기화
pygame.init()
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball")

# 색상
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

# 공 설정
ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 4   # x 방향 속도
ball_dy = 3   # y 방향 속도

clock = pygame.time.Clock()
running = True