import os
import json
import math
import pygame
import re

# === 기본 설정 ===
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("미로 탐험형 - JSON 스테이지 로더")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WALL  = (35, 35, 35)
PATH  = (230, 230, 230)
GOAL  = (70, 170, 255)
START = (255, 200, 0)
YELLOW = (255, 244, 79)
BLUE   = (0, 120, 255)