import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame-6: Ultimate Archery")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DARK_BLUE = (0, 50, 150)
BOW_BROWN = (100, 50, 0)

# 폰트 설정
try:
    FONT_PATH = r"C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\Open Font License\KCC한빛체\KCC한빛체\KCC-Hanbit.ttf"
    font = pygame.font.Font(FONT_PATH, 20)
    score_font = pygame.font.Font(FONT_PATH, 35)
except:
    font = pygame.font.SysFont("arial", 20)
    score_font = pygame.font.SysFont("arial", 35)

# 플레이어 & 적 설정
PLAYER_SIZE = 50
PLAYER_SPEED = 5
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

ENEMY_SIZE = 50
ENEMY_SPEED = 3

def get_random_outside_pos():
    OFFSET = 60 
    side = random.randint(0, 3)
    if side == 0: return pygame.Vector2(random.randint(-OFFSET, WIDTH+OFFSET), -OFFSET)
    elif side == 1: return pygame.Vector2(random.randint(-OFFSET, WIDTH+OFFSET), HEIGHT+OFFSET)
    elif side == 2: return pygame.Vector2(-OFFSET, random.randint(-OFFSET, HEIGHT+OFFSET))
    else: return pygame.Vector2(WIDTH+OFFSET, random.randint(-OFFSET, HEIGHT+OFFSET))

enemy_pos = get_random_outside_pos()
enemy_move_timer = pygame.time.get_ticks()
enemy_is_moving = True

# 게임 상태 변수
score = 0
MAX_DRAG = 200
dragging = False
press_pos = pygame.Vector2(0, 0)
projectiles = []
can_move = True

class Projectile:
    def __init__(self, pos, velocity, level):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(velocity)
        self.level = level
    def update(self):
        self.pos += self.vel
        self.vel *= 0.99 
    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.pos.x), int(self.pos.y)), 6)

clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks()
    current_level = 0
    screen.fill(WHITE)
    
    # --- 1. 이벤트 처리 ---
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
            
            if drag_vec.length() > 20:
                if drag_vec.length() > MAX_DRAG: drag_vec = drag_vec.normalize() * MAX_DRAG
                level = max(0, min(int(drag_vec.length() / (MAX_DRAG/10)), 10))
                
                if level >= 2:
                    speed_table = [0, 0, 8, 10, 12, 14, 16, 18, 20, 22, 25]
                    speed = speed_table[level]
                    velocity = -drag_vec.normalize() * speed
                    projectiles.append(Projectile(player_pos + pygame.Vector2(25, 25), velocity, level))

    # --- 2. 플레이어 상태 및 이동 (패널티 포함) ---
    can_move = True
    if dragging:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        drag_vec = mouse_pos - press_pos
        if drag_vec.length() > MAX_DRAG: drag_vec = drag_vec.normalize() * MAX_DRAG
        current_level = int(drag_vec.length() / (MAX_DRAG / 10))
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

    # --- 3. 적 AI (외부 진입 및 정지 패턴) ---
    if current_time - enemy_move_timer > 2000:
        enemy_is_moving = not enemy_is_moving
        enemy_move_timer = current_time

    if enemy_is_moving:
        player_center = player_pos + pygame.Vector2(25, 25)
        enemy_center = enemy_pos + pygame.Vector2(25, 25)
        dir_to_player = player_center - enemy_center
        if dir_to_player.length() > 0:
            enemy_pos += dir_to_player.normalize() * ENEMY_SPEED

    # --- 4. 업데이트 및 충돌 (점수 시스템) ---
    for p in projectiles[:]:
        p.update()
        enemy_center = enemy_pos + pygame.Vector2(25, 25)
        if p.pos.distance_to(enemy_center) < (25 + 6):
            score += 100 + (p.level * 20)
            projectiles.remove(p)
            enemy_pos = get_random_outside_pos() # 명중 시 외부 재스폰
        elif p.pos.x < -100 or p.pos.x > WIDTH + 100 or p.pos.y < -100 or p.pos.y > HEIGHT + 100:
            projectiles.remove(p)

    # --- 5. 화면 그리기 ---
    # 점수 표시
    score_surf = score_font.render(f"SCORE: {score}", True, BLACK)
    screen.blit(score_surf, (WIDTH - 250, 20))

    # 플레이어 & 적
    p_color = BLUE if can_move else DARK_BLUE
    pygame.draw.rect(screen, p_color, (player_pos.x, player_pos.y, 50, 50))
    pygame.draw.rect(screen, RED, (enemy_pos.x, enemy_pos.y, 50, 50))
    if not enemy_is_moving:
        pygame.draw.rect(screen, BLACK, (enemy_pos.x, enemy_pos.y, 50, 50), 3)

    # 조준 시각 효과 (화살촉 + 활시위 + 게이지)
    if dragging:
        center = player_pos + pygame.Vector2(25, 25)
        aim_dir = -drag_vec.normalize() if drag_vec.length() > 0 else pygame.Vector2(0, -1)
        aim_end = center + aim_dir * drag_vec.length()
        tension_color = RED if not can_move else BLACK
        
        # 1) 활시위(String)와 활 몸체(Bow)
        perp_vec = pygame.Vector2(-aim_dir.y, aim_dir.x) * 35
        bow_start = center + (aim_dir * 15) + perp_vec
        bow_end = center + (aim_dir * 15) - perp_vec
        pygame.draw.line(screen, GRAY, bow_start, pygame.mouse.get_pos(), 1) # 시위 상단
        pygame.draw.line(screen, GRAY, bow_end, pygame.mouse.get_pos(), 1)   # 시위 하단
        pygame.draw.line(screen, BOW_BROWN, bow_start, bow_end, 5)           # 활 몸체
        
        # 2) 화살 조준선 및 화살촉
        pygame.draw.line(screen, tension_color, center, aim_end, 2)
        if drag_vec.length() > 20:
            wing_l = aim_end + aim_dir.rotate(150) * 15
            wing_r = aim_end + aim_dir.rotate(-150) * 15
            pygame.draw.polygon(screen, tension_color, [aim_end, wing_l, wing_r])

        # 3) 기존 파워 게이지 바 (플레이어 머리 위)
        gauge_width = (drag_vec.length() / MAX_DRAG) * 50
        pygame.draw.rect(screen, GRAY, (player_pos.x, player_pos.y - 15, 50, 8))
        pygame.draw.rect(screen, (BLUE if can_move else RED), (player_pos.x, player_pos.y - 15, gauge_width, 8))

    # 하단 정보 텍스트
    status_msg = f"Power: {current_level} | Enemy: {'MOVING' if enemy_is_moving else 'STOPPED'}"
    level_text = font.render(status_msg, True, BLACK if can_move else RED)
    screen.blit(level_text, (20, 20))

    for p in projectiles:
        p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()