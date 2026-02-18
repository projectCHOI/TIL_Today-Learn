import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame-6: Multiple Enemies System")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
DARK_BLUE = (0, 50, 150)

# 폰트 설정
try:
    FONT_PATH = r"C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\Open Font License\KCC한빛체\KCC한빛체\KCC-Hanbit.ttf"
    font = pygame.font.Font(FONT_PATH, 20)
    score_font = pygame.font.Font(FONT_PATH, 35)
except:
    font = pygame.font.SysFont("arial", 20)
    score_font = pygame.font.SysFont("arial", 35)

# 플레이어 설정
PLAYER_SIZE = 50
PLAYER_SPEED = 5
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

# 적(Enemy) 설정
ENEMY_SIZE = 50
ENEMY_SPEED = 2.5
NUM_ENEMIES = 5  # 동시에 존재할 적의 수

def get_random_outside_pos():
    """8방향 무작위 외부 스폰 로직 유지"""
    OFFSET = 60 
    side = random.randint(0, 3)
    if side == 0: return pygame.Vector2(random.randint(-OFFSET, WIDTH+OFFSET), -OFFSET)
    elif side == 1: return pygame.Vector2(random.randint(-OFFSET, WIDTH+OFFSET), HEIGHT+OFFSET)
    elif side == 2: return pygame.Vector2(-OFFSET, random.randint(-OFFSET, HEIGHT+OFFSET))
    else: return pygame.Vector2(WIDTH+OFFSET, random.randint(-OFFSET, HEIGHT+OFFSET))

# [수정] 적들을 리스트로 관리
enemies = []
for _ in range(NUM_ENEMIES):
    enemies.append(get_random_outside_pos())

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
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
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
                    speed = [0, 0, 8, 10, 12, 14, 16, 18, 20, 22, 25][level]
                    projectiles.append(Projectile(player_pos + pygame.Vector2(25, 25), -drag_vec.normalize() * speed, level))

    # 플레이어 상태 및 이동 (기존 기능 유지)
    can_move, current_level = True, 0
    if dragging:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        drag_vec = mouse_pos - press_pos
        drag_dist = min(drag_vec.length(), MAX_DRAG)
        current_level = int(drag_dist / (MAX_DRAG / 10))
        if current_level >= 10: can_move = False

    if can_move:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player_pos.y -= PLAYER_SPEED
        if keys[pygame.K_s]: player_pos.y += PLAYER_SPEED
        if keys[pygame.K_a]: player_pos.x -= PLAYER_SPEED
        if keys[pygame.K_d]: player_pos.x += PLAYER_SPEED
    
    player_pos.x = max(0, min(player_pos.x, WIDTH - 50))
    player_pos.y = max(0, min(player_pos.y, HEIGHT - 50))

    # --- [수정] 적 AI 및 업데이트 (다중 적 대응) ---
    if current_time - enemy_move_timer > 2000:
        enemy_is_moving = not enemy_is_moving
        enemy_move_timer = current_time

    player_center = player_pos + pygame.Vector2(25, 25)
    for i in range(len(enemies)):
        if enemy_is_moving:
            enemy_center = enemies[i] + pygame.Vector2(25, 25)
            dir_p = player_center - enemy_center
            if dir_p.length() > 0:
                enemies[i] += dir_p.normalize() * ENEMY_SPEED

    # --- [수정] 충돌 체크 (다중 적 대응) ---
    for p in projectiles[:]:
        p.update()
        hit_enemy = False
        for i in range(len(enemies)):
            enemy_center = enemies[i] + pygame.Vector2(25, 25)
            if p.pos.distance_to(enemy_center) < 31:
                score += 100 + (p.level * 20)
                enemies[i] = get_random_outside_pos() # 맞은 적만 새로 생성
                hit_enemy = True
                break
        if hit_enemy:
            projectiles.remove(p)
        elif not screen.get_rect().collidepoint(p.pos):
            projectiles.remove(p)

    # --- 화면 그리기 ---
    screen.blit(score_font.render(f"SCORE: {score}", True, BLACK), (WIDTH - 250, 20))
    
    # 플레이어 그리기
    pygame.draw.rect(screen, BLUE if can_move else DARK_BLUE, (player_pos.x, player_pos.y, 50, 50))
    
    # [수정] 모든 적 그리기
    for e_pos in enemies:
        pygame.draw.rect(screen, RED, (e_pos.x, e_pos.y, 50, 50))
        if not enemy_is_moving:
            pygame.draw.rect(screen, BLACK, (e_pos.x, e_pos.y, 50, 50), 3)

    # 🏹 조준 가이드 (기존 60% 축소 버전 유지)
    if dragging:
        center = player_pos + pygame.Vector2(25, 25)
        guide_color = RED if current_level >= 10 else GREEN
        guide_radius = 30 + (drag_dist * 0.3) 
        
        pygame.draw.circle(screen, guide_color, (int(center.x), int(center.y)), int(guide_radius), 2)
        pygame.draw.line(screen, guide_color, (center.x - guide_radius, center.y), (center.x + guide_radius, center.y), 1)
        pygame.draw.line(screen, guide_color, (center.x, center.y - guide_radius), (center.x, center.y + guide_radius), 1)

        if drag_vec.length() > 0:
            aim_dir = -drag_vec.normalize()
            dash_len, dash_gap = 4, 4
            num_dashes = int(guide_radius / (dash_len + dash_gap))
            for i in range(num_dashes):
                d_start_dist = i * (dash_len + dash_gap)
                d_end_dist = d_start_dist + dash_len
                if d_end_dist > guide_radius: d_end_dist = guide_radius
                pygame.draw.line(screen, guide_color, center + aim_dir * d_start_dist, center + aim_dir * d_end_dist, 2)

            arrow_pos = center + aim_dir * guide_radius
            wing_l = arrow_pos + aim_dir.rotate(150) * 10
            wing_r = arrow_pos + aim_dir.rotate(-150) * 10
            pygame.draw.polygon(screen, guide_color, [arrow_pos, wing_l, wing_r])

    # 정보 표시
    status_msg = f"Power: {current_level} | Enemies: {NUM_ENEMIES}"
    screen.blit(font.render(status_msg, True, BLACK if can_move else RED), (20, 20))
    for p in projectiles: p.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()