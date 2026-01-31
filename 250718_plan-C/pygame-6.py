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
BLUE = (0, 100, 255)

# 폰트
FONT_PATH = r"C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\Open Font License\KCC한빛체\KCC한빛체\KCC-Hanbit.ttf"
font = pygame.font.Font(FONT_PATH, 20)
# 플레이어
PLAYER_SIZE = 50
PLAYER_SPEED = 5
player_x = WIDTH // 2
player_y = HEIGHT // 2

# 투사체 설정
PROJECTILE_RADIUS = 6

# 파워 단계 설정
MAX_DRAG = 200
MAX_LEVEL = 10
POWER_TABLE = [0, 0, 8, 10, 12, 14, 16, 18, 20, 22, 25]

# 드래그 상태
dragging = False
press_pos = (0, 0)
current_pos = (0, 0)

projectiles = []

clock = pygame.time.Clock()
running = True

class Projectile:
    def __init__(self, pos, velocity):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(velocity)

    def update(self):
        self.pos += self.vel
        self.vel *= 0.99  # 간단한 감속

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, self.pos, PROJECTILE_RADIUS)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 드래그 시작
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            press_pos = pygame.mouse.get_pos()
        # 드래그 종료 → 발사
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
            release_pos = pygame.mouse.get_pos()
#
            mouse_pos = pygame.mouse.get_pos()
            drag_vec = pygame.Vector2(mouse_pos) - pygame.Vector2(press_pos)

            if drag_vec.length() > MAX_DRAG:
                drag_vec = drag_vec.normalize() * MAX_DRAG

            aim_end = pygame.Vector2(press_pos) + drag_vec

            pygame.draw.line(
                screen,
                BLACK,
                (player_x + PLAYER_SIZE // 2, player_y + PLAYER_SIZE // 2),
                aim_end,
                2
            )
#
            # 거리 → 단계
            level = int(drag_dist / (MAX_DRAG / MAX_LEVEL))
            level = max(0, min(level, MAX_LEVEL))

            if level >= 2:
                direction = -drag_vec.normalize()
                speed = POWER_TABLE[level]
                velocity = direction * speed

                projectiles.append(
                    Projectile(
                        (player_x + PLAYER_SIZE // 2, player_y + PLAYER_SIZE // 2),
                        velocity
                    )
                )
    # 플레이어 이동
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
    # 투사체 업데이트
    for p in projectiles:
        p.update()
    # 화면 그리기
    screen.fill(WHITE)
    # 플레이어
    pygame.draw.rect(
        screen,
        RED,
        (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    )
    # 에임 가이드
    if dragging:
        current_pos = pygame.mouse.get_pos()
        pygame.draw.line(
            screen,
            BLACK,
            (player_x + PLAYER_SIZE // 2, player_y + PLAYER_SIZE // 2),
            current_pos,
            2
        )
        # 단계 표시
        drag_dist = pygame.Vector2(current_pos).distance_to(press_pos)
        level = int(drag_dist / (MAX_DRAG / MAX_LEVEL))
        level = max(0, min(level, MAX_LEVEL))
        level_text = font.render(f"Power Level: {level}", True, BLACK)
        screen.blit(level_text, (20, 20))
    # 투사체
    for p in projectiles:
        p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()