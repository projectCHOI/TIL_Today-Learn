# 오목게임
import pygame
# --- 설정 값 ---
BOARD_SIZE = 15  # 15x15 바둑판
GRID_SIZE = 40   # 그리드 한 칸의 크기
MARGIN = 40      # 테두리 여백
SCREEN_SIZE = GRID_SIZE * (BOARD_SIZE - 1) + MARGIN * 2

# 색상 정의
COLOR_BOARD = (220, 179, 92)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_LINE = (0, 0, 0)