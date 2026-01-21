import pygame
import sys

# pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Project")

# 색상 정의
WHITE = (255, 255, 255)

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 배경 채우기 (흰색)
    screen.fill(WHITE)

    # 화면 업데이트
    pygame.display.flip()

# pygame 종료
pygame.quit()
sys.exit()
