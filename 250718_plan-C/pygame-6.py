import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame-6: Penalty System")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GRAY = (200, 200, 200)
DARK_RED = (150, 0, 0) # 패널티 상태 표시용

# 폰트 설정
try:
    FONT_PATH = r"C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\Open Font License\KCC한빛체\KCC한빛체\KCC-Hanbit.ttf"
    font = pygame.font.Font(FONT_PATH, 20)
except:
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
can_move = True # 이동 가능 여부 플래그

class Projectile:
    def __init__(self, pos, velocity):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(velocity)

    def update(self):
        self.pos += self.vel
        self.vel *= 0.99 

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, self.pos, PROJECTILE_RADIUS)

clock = pygame.time.Clock()
running = True

while running:
    # --- 1. 이벤트 처리 ---
    current_level = 0 # 루프마다 레벨 계산 초기화
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            press_pos = pygame.Vector2(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
            release_pos = pygame.Vector2(pygame.mouse.get_pos())
            drag_vec = release_pos - press_pos
            
            if drag_vec.length() > 0:
                if drag_vec.length() > MAX_DRAG:
                    drag_vec = drag_vec.normalize() * MAX_DRAG

                level = int(drag_vec.length() / (MAX_DRAG / MAX_LEVEL))
                level = max(0, min(level, MAX_LEVEL))

                if level >= 2:
                    direction = -drag_vec.normalize()
                    speed = POWER_TABLE[level]
                    velocity = direction * speed
                    projectiles.append(
                        Projectile(player_pos + pygame.Vector2(PLAYER_SIZE // 2, PLAYER_SIZE // 2), velocity)
                    )

    # --- 2. 실시간 상태 체크 (드래그 중 레벨 계산) ---
    can_move = True # 기본적으로 이동 가능
    if dragging:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        drag_vec = mouse_pos - press_pos
        current_dist = min(drag_vec.length(), MAX_DRAG)
        current_level = int(current_dist / (MAX_DRAG / MAX_LEVEL))
        
        # 패널티 조건: 파워 레벨이 10이면 이동 불가
        if current_level >= 10:
            can_move = False

    # --- 3. 플레이어 이동 로직 (패널티 적용) ---
    if can_move:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player_pos.y -= PLAYER_SPEED
        if keys[pygame.K_s]: player_pos.y += PLAYER_SPEED
        if keys[pygame.K_a]: player_pos.x -= PLAYER_SPEED
        if keys[pygame.K_d]: player_pos.x += PLAYER_SPEED
    
    player_pos.x = max(0, min(player_pos.x, WIDTH - PLAYER_SIZE))
    player_pos.y = max(0, min(player_pos.y, HEIGHT - PLAYER_SIZE))

    # --- 4. 업데이트 ---
    for p in projectiles[:]:
        p.update()
        if p.pos.x < 0 or p.pos.x > WIDTH or p.pos.y < 0 or p.pos.y > HEIGHT:
            projectiles.remove(p)

    # --- 5. 화면 그리기 ---
    screen.fill(WHITE)

    # 플레이어 색상 변경 (이동 불가 시 어두운 빨간색)
    p_color = RED if can_move else DARK_RED
    pygame.draw.rect(screen, p_color, (player_pos.x, player_pos.y, PLAYER_SIZE, PLAYER_SIZE))

    # 에임 가이드 및 게이지
    if dragging:
        center = player_pos + pygame.Vector2(PLAYER_SIZE // 2, PLAYER_SIZE // 2)
        # 실제 제한된 벡터로 가이드 표시
        display_vec = (pygame.Vector2(pygame.mouse.get_pos()) - press_pos)
        if display_vec.length() > MAX_DRAG: display_vec = display_vec.normalize() * MAX_DRAG
        
        pygame.draw.line(screen, BLACK, center, center - display_vec, 2)
        
        # 파워 게이지
        gauge_width = (display_vec.length() / MAX_DRAG) * PLAYER_SIZE
        pygame.draw.rect(screen, GRAY, (player_pos.x, player_pos.y - 15, PLAYER_SIZE, 8))
        gauge_color = BLUE if can_move else RED # 풀파워 시 게이지도 빨간색으로 변경
        pygame.draw.rect(screen, gauge_color, (player_pos.x, player_pos.y - 15, gauge_width, 8))

    # 상태 텍스트
    status_msg = f"Power Level: {current_level}"
    if not can_move:
        status_msg += " (MOVE OVERLOAD!)"
    
    level_text = font.render(status_msg, True, BLACK if can_move else RED)
    screen.blit(level_text, (20, 20))

    for p in projectiles:
        p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()