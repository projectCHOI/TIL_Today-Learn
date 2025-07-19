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

# 게임 루프
clock = pygame.time.Clock()
run = True
score = 0

while run:
    clock.tick(30)
    win.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < win_width - player_size:
        player_pos[0] += player_speed

    # 적 이동
    enemy_pos[1] += enemy_speed
    if enemy_pos[1] > win_height:
        enemy_pos[1] = 0
        enemy_pos[0] = random.randint(0, win_width - enemy_size)
        score += 1
        enemy_speed += 0.5  # 난이도 증가

    # 충돌 체크
    if detect_collision(player_pos, enemy_pos):
        text = font.render("Game Over!", True, RED)
        win.blit(text, (win_width//2 - 100, win_height//2 - 20))
        pygame.display.update()
        pygame.time.delay(2000)
        run = False

    # 그리기
    pygame.draw.rect(win, BLUE, (*player_pos, player_size, player_size))
    pygame.draw.rect(win, RED, (*enemy_pos, enemy_size, enemy_size))

    # 점수 표시
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    win.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
sys.exit()