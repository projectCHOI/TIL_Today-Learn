import pygame
import sys

# pygame 초기화
pygame.init()

# 화면 크기
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame-6")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# === 폰트 경로 ===
FONT_PATH = r"C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\Open Font License\KCC한빛체\KCC한빛체\KCC-Hanbit.ttf"

# 폰트 객체 생성
font = pygame.font.Font(FONT_PATH, 32)  # 32 = 폰트 크기

# 텍스트 생성
text_surface = font.render("Pygame + KCC 한빛체", True, BLACK)
text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 배경
    screen.fill(WHITE)

    # 텍스트 그리기
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)  # FPS 제한

pygame.quit()
sys.exit()
