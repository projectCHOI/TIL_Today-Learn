# 오목게임
import pygame
# --- 설정 값 ---
BOARD_SIZE = 15 
GRID_SIZE = 40 
MARGIN = 40 
SCREEN_SIZE = GRID_SIZE * (BOARD_SIZE - 1) + MARGIN * 2

# 색상 정의
COLOR_BOARD = (220, 179, 92)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_LINE = (0, 0, 0)

class OmokGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Python Omok Game")
        self.clock = pygame.time.Clock()

        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.turn = 1  # 1: 흑, 2: 백
        self.game_over = False