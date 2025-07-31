import pygame
import sys

# 초기화
pygame.init()
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")

# 색상
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)

# 플레이어 설정
player_width, player_height = 40, 50
player_x, player_y = 100, HEIGHT - player_height - 50
player_speed = 5
player_vel_y = 0
gravity = 0.5
jump_power = -10
on_ground = False

# 플랫폼 설정
platforms = [
    pygame.Rect(0, HEIGHT - 40, WIDTH, 40),      # 바닥
    pygame.Rect(150, 300, 100, 20),
    pygame.Rect(300, 220, 120, 20),
    pygame.Rect(480, 150, 100, 20),
]
