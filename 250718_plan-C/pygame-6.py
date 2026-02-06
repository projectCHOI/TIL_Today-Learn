import pygame
import sys
import math

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame-6: Drag & Shoot")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GRAY = (200, 200, 200)

# 폰트 설정
try:
    FONT_PATH = r"C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\Open Font License\KCC한빛체\KCC한빛체\KCC-Hanbit.ttf"
    font = pygame.font.Font(FONT_PATH, 20)
except:
    print("폰트 파일을 찾을 수 없습니다.")
    font = pygame.font.SysFont("arial", 20)

# 플레이어 설정
PLAYER_SIZE = 50
PLAYER_SPEED = 5
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

# 투사체 설정
PROJECTILE_RADIUS = 6
MAX_DRAG = 200
MAX_LEVEL = 10
POWER_TABLE = [0, 0, 8, 10, 12, 14, 16, 18, 20, 22, 25]

# 상태 변수
dragging = False
press_pos = pygame.Vector2(0, 0)
projectiles = []

class Projectile:
    def __init__(self, pos, velocity):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(velocity)

    def update(self):
        self.pos += self.vel
        self.vel *= 0.99  # 마찰력(감속)

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, self.pos, PROJECTILE_RADIUS)

clock = pygame.time.Clock()
running = True

while running:
    # --- 1. 이벤트 처리 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 드래그 시작
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            press_pos = pygame.Vector2(pygame.mouse.get_pos())

        # 드래그 종료 -> 발사
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
            release_pos = pygame.Vector2(pygame.mouse.get_pos())
            
            drag_vec = release_pos - press_pos
            
            if drag_vec.length() > 0:
                # 최대 드래그 거리 제한
                if drag_vec.length() > MAX_DRAG:
                    drag_vec = drag_vec.normalize() * MAX_DRAG

                drag_dist = drag_vec.length()
                level = int(drag_dist / (MAX_DRAG / MAX_LEVEL))
                level = max(0, min(level, MAX_LEVEL))

                # 레벨 2 이상일 때만 발사 (실수 방지)
                if level >= 2:
                    direction = -drag_vec.normalize() # 슬링샷 방식 (반대 방향)
                    speed = POWER_TABLE[level]
                    velocity = direction * speed

                    projectiles.append(
                        Projectile(
                            player_pos + pygame.Vector2(PLAYER_SIZE // 2, PLAYER_SIZE // 2),
                            velocity
                        )
                    )

    # --- 2. 플레이어 이동 로직 ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player_pos.y -= PLAYER_SPEED
    if keys[pygame.K_s]: player_pos.y += PLAYER_SPEED
    if keys[pygame.K_a]: player_pos.x -= PLAYER_SPEED
    if keys[pygame.K_d]: player_pos.x += PLAYER_SPEED
    
    # 화면 경계 제한
    player_pos.x = max(0, min(player_pos.x, WIDTH - PLAYER_SIZE))
    player_pos.y = max(0, min(player_pos.y, HEIGHT - PLAYER_SIZE))

    # --- 3. 투사체 업데이트 및 화면 밖 제거 ---
    for p in projectiles[:]:
        p.update()
        # 화면 경계를 벗어나면 리스트에서 삭제 (메모리 관리)
        if p.pos.x < 0 or p.pos.x > WIDTH or p.pos.y < 0 or p.pos.y > HEIGHT:
            projectiles.remove(p)
        # 속도가 거의 멈추면 삭제 (옵션)
        elif p.vel.length() < 0.2:
            projectiles.remove(p)

    # --- 4. 화면 그리기 ---
    screen.fill(WHITE)

    # 플레이어 그리기
    pygame.draw.rect(screen, RED, (player_pos.x, player_pos.y, PLAYER_SIZE, PLAYER_SIZE))

    # 에임 가이드 및 파워 게이지
    if dragging:
        current_mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        drag_vec = current_mouse_pos - press_pos
        
        if drag_vec.length() > MAX_DRAG:
            drag_vec = drag_vec.normalize() * MAX_DRAG
        
        # 1) 조준선 표시
        center = player_pos + pygame.Vector2(PLAYER_SIZE // 2, PLAYER_SIZE // 2)
        aim_end = center - drag_vec # 발사될 방향 표시
        pygame.draw.line(screen, BLACK, center, aim_end, 2)
        
        # 2) 파워 게이지 (플레이어 머리 위)
        drag_dist = drag_vec.length()
        level = int(drag_dist / (MAX_DRAG / MAX_LEVEL))
        gauge_width = (drag_dist / MAX_DRAG) * PLAYER_SIZE
        
        pygame.draw.rect(screen, GRAY, (player_pos.x, player_pos.y - 15, PLAYER_SIZE, 8)) # 배경
        pygame.draw.rect(screen, BLUE, (player_pos.x, player_pos.y - 15, gauge_width, 8)) # 게이지

    # 텍스트 정보
    level_val = 0
    if dragging:
        level_val = max(0, min(int(drag_vec.length() / (MAX_DRAG / MAX_LEVEL)), MAX_LEVEL))
    level_text = font.render(f"Power Level: {level_val}", True, BLACK)
    screen.blit(level_text, (20, 20))

    # 투사체 그리기
    for p in projectiles:
        p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()