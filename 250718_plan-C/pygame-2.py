import pygame
import random
import sys

# 초기화
pygame.init()
win_width, win_height = 500, 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("충돌 회피 게임")

# 색상
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# 플레이어 설정
player_size = 50
player_pos = [win_width // 2, win_height - player_size - 10]
player_speed = 7

# 적 설정
enemy_size = 50
enemy_pos = [random.randint(0, win_width - enemy_size), 0]
enemy_speed = 5

# 폰트
font = pygame.font.SysFont("comicsans", 40)

# 충돌 감지 함수
def detect_collision(player_pos, enemy_pos):
    px, py = player_pos
    ex, ey = enemy_pos

    return (
        px < ex + enemy_size and
        px + player_size > ex and
        py < ey + enemy_size and
        py + player_size > ey
    )