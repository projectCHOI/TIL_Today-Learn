import pygame
import sys
import math

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame-6")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# === 폰트 경로 ===
FONT_PATH = r"C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\Open Font License\KCC한빛체\KCC한빛체\KCC-Hanbit.ttf"
font = pygame.font.Font(FONT_PATH, 24)
# 플레이어 설정
PLAYER_SIZE = 50
PLAYER_SPEED = 5
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT // 2 - PLAYER_SIZE // 2

# 텍스트 생성
text_surface = font.render("Pygame", True, BLACK)
text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_s]:
        player_y += PLAYER_SPEED
    if keys[pygame.K_a]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_d]:
        player_x += PLAYER_SPEED

    player_x = max(0, min(player_x, WIDTH - PLAYER_SIZE))
    player_y = max(0, min(player_y, HEIGHT - PLAYER_SIZE))

    # 배경
    screen.fill(WHITE)

    pygame.draw.rect(
        screen,
        RED,
        (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    )

    # 텍스트 그리기
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
