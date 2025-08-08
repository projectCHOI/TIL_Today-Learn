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

pygame.quit()
sys.exit()