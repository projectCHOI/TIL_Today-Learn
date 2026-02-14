import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame-6: Score System")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DARK_BLUE = (0, 50, 150)
GOLD = (255, 215, 0) # 고득점 강조색

# 폰트 설정
try:
    FONT_PATH = r"C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\Open Font License\KCC한빛체\KCC한빛체\KCC-Hanbit.ttf"
    font = pygame.font.Font(FONT_PATH, 20)
    score_font = pygame.font.Font(FONT_PATH, 35) # 점수용 큰 폰트
except:
    font = pygame.font.SysFont("arial", 20)
    score_font = pygame.font.SysFont("arial", 35)

# 플레이어 설정
PLAYER_SIZE = 50
PLAYER_SPEED = 5
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

# 적(Target) 설정
ENEMY_SIZE = 50
ENEMY_SPEED = 3
enemy_pos = pygame.Vector2(100, 100)
enemy_move_timer = pygame.time.get_ticks()
enemy_is_moving = True

# 점수 설정
score = 0
last_hit_score = 0
hit_effect_timer = 0

# 투사체 설정
PROJECTILE_RADIUS = 6
MAX_DRAG = 200
MAX_LEVEL = 10
POWER_TABLE = [0, 0, 8, 10, 12, 14, 16, 18, 20, 22, 25]

# 상태 변수
dragging = False
press_pos = pygame.Vector2(0, 0)
projectiles = []
can_move = True

class Projectile:
    def __init__(self, pos, velocity, level):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(velocity)
        self.level = level # 발사 시 파워 레벨 저장

    def update(self):
        self.pos += self.vel
        self.vel *= 0.99 

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, self.pos, PROJECTILE_RADIUS)

clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks()
    current_level = 0
    
    # --- 1. 이벤트 처리 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            press_pos = pygame.Vector2(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
            release_pos = pygame.mouse.get_pos()
            drag_vec = pygame.Vector2(release_pos) - press_pos
            
            if drag_vec.length() > 0:
                if drag_vec.length() > MAX_DRAG:
                    drag_vec = drag_vec.normalize() * MAX_DRAG

                level = int(drag_vec.length() / (MAX_DRAG / MAX_LEVEL))
                level = max(0, min(level, MAX_LEVEL))

                if level >= 2:
                    direction = -drag_vec.normalize()
                    speed = POWER_TABLE[level]
                    velocity = direction * speed
                    # 생성 시 레벨 정보 전달
                    projectiles.append(
                        Projectile(player_pos + pygame.Vector2(PLAYER_SIZE // 2, PLAYER_SIZE // 2), velocity, level)
                    )

    # --- 2. 플레이어 상태 및 이동 ---
    can_move = True
    if dragging:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        drag_vec = mouse_pos - press_pos
        current_dist = min(drag_vec.length(), MAX_DRAG)
        current_level = int(current_dist / (MAX_DRAG / MAX_LEVEL))
        if current_level >= 10:
            can_move = False

    if can_move:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player_pos.y -= PLAYER_SPEED
        if keys[pygame.K_s]: player_pos.y += PLAYER_SPEED
        if keys[pygame.K_a]: player_pos.x -= PLAYER_SPEED
        if keys[pygame.K_d]: player_pos.x += PLAYER_SPEED
    
    player_pos.x = max(0, min(player_pos.x, WIDTH - PLAYER_SIZE))
    player_pos.y = max(0, min(player_pos.y, HEIGHT - PLAYER_SIZE))

    # --- 3. 적(Target) AI ---
    if current_time - enemy_move_timer > 2000:
        enemy_is_moving = not enemy_is_moving
        enemy_move_timer = current_time

    if enemy_is_moving:
        player_center = player_pos + pygame.Vector2(PLAYER_SIZE/2, PLAYER_SIZE/2)
        enemy_center = enemy_pos + pygame.Vector2(ENEMY_SIZE/2, ENEMY_SIZE/2)
        dir_to_player = player_center - enemy_center
        if dir_to_player.length() > 0:
            enemy_pos += dir_to_player.normalize() * ENEMY_SPEED

    # --- 4. 업데이트 및 충돌 (점수 획득) ---
    for p in projectiles[:]:
        p.update()
        
        enemy_center = enemy_pos + pygame.Vector2(ENEMY_SIZE/2, ENEMY_SIZE/2)
        if p.pos.distance_to(enemy_center) < (ENEMY_SIZE/2 + PROJECTILE_RADIUS):
            # 점수 계산: (기본 100점) + (파워 레벨 * 20점)
            gain_score = 100 + (p.level * 20)
            score += gain_score
            
            # 피드백용 변수 설정
            last_hit_score = gain_score
            hit_effect_timer = current_time 
            
            projectiles.remove(p)
            # 적 재배치
            enemy_pos = pygame.Vector2(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50))

        elif p.pos.x < 0 or p.pos.x > WIDTH or p.pos.y < 0 or p.pos.y > HEIGHT:
            projectiles.remove(p)

    # --- 5. 화면 그리기 ---
    screen.fill(WHITE)

    # 점수 표시 (우측 상단)
    score_surf = score_font.render(f"SCORE: {score}", True, BLACK)
    screen.blit(score_surf, (WIDTH - 250, 20))

    # 명중 시 점수 팝업 효과 (0.5초간 표시)
    if current_time - hit_effect_timer < 500:
        hit_text = font.render(f"+{last_hit_score}!", True, RED)
        screen.blit(hit_text, (enemy_pos.x, enemy_pos.y - 30))

    # 플레이어 & 적 그리기
    p_color = BLUE if can_move else DARK_BLUE
    pygame.draw.rect(screen, p_color, (player_pos.x, player_pos.y, PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.rect(screen, RED, (enemy_pos.x, enemy_pos.y, ENEMY_SIZE, ENEMY_SIZE))
    
    if not enemy_is_moving:
        pygame.draw.rect(screen, BLACK, (enemy_pos.x, enemy_pos.y, ENEMY_SIZE, ENEMY_SIZE), 3)

    # 에임 가이드
    if dragging:
        center = player_pos + pygame.Vector2(PLAYER_SIZE // 2, PLAYER_SIZE // 2)
        display_vec = (pygame.Vector2(pygame.mouse.get_pos()) - press_pos)
        if display_vec.length() > MAX_DRAG: display_vec = display_vec.normalize() * MAX_DRAG
        pygame.draw.line(screen, BLACK, center, center - display_vec, 2)
        
        gauge_width = (display_vec.length() / MAX_DRAG) * PLAYER_SIZE
        pygame.draw.rect(screen, GRAY, (player_pos.x, player_pos.y - 15, PLAYER_SIZE, 8))
        gauge_color = BLUE if can_move else RED
        pygame.draw.rect(screen, gauge_color, (player_pos.x, player_pos.y - 15, gauge_width, 8))

    # 하단 정보
    status_msg = f"Power: {current_level} | Enemy: {'MOVING' if enemy_is_moving else 'STOPPED'}"
    level_text = font.render(status_msg, True, BLACK if can_move else RED)
    screen.blit(level_text, (20, 20))

    for p in projectiles:
        p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()