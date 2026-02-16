import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame-6: Dynamic Aiming Guide")

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

# 플레이어 & 적 설정 (기존 로직 유지)
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
MAX_DRAG = 200 # 강도 10의 기준점
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

    # --- 플레이어 상태 및 이동 ---
    can_move = True
    current_level = 0
    if dragging:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        drag_vec = mouse_pos - press_pos
        drag_dist = min(drag_vec.length(), MAX_DRAG)
        current_level = int(drag_dist / (MAX_DRAG / 10))
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

    # --- 적 AI 및 업데이트 ---
    if current_time - enemy_move_timer > 2000:
        enemy_is_moving = not enemy_is_moving
        enemy_move_timer = current_time
    if enemy_is_moving:
        dir_to_p = (player_pos + pygame.Vector2(25, 25)) - (enemy_pos + pygame.Vector2(25, 25))
        if dir_to_p.length() > 0:
            enemy_pos += dir_to_p.normalize() * ENEMY_SPEED

    for p in projectiles[:]:
        p.update()
        if p.pos.distance_to(enemy_pos + pygame.Vector2(25, 25)) < 31:
            score += 100 + (p.level * 20)
            projectiles.remove(p)
            enemy_pos = get_random_outside_pos()
        elif not screen.get_rect().collidepoint(p.pos):
            projectiles.remove(p)

    # --- 화면 그리기 ---
    # 점수 표시
    screen.blit(score_font.render(f"SCORE: {score}", True, BLACK), (WIDTH - 250, 20))

    # 플레이어 & 적
    p_color = BLUE if can_move else DARK_BLUE
    pygame.draw.rect(screen, p_color, (player_pos.x, player_pos.y, 50, 50))
    pygame.draw.rect(screen, RED, (enemy_pos.x, enemy_pos.y, 50, 50))
    if not enemy_is_moving:
        pygame.draw.rect(screen, BLACK, (enemy_pos.x, enemy_pos.y, 50, 50), 3)

    # 🏹 [핵심 업데이트] 조준 가이드 시각 효과
    if dragging:
        center = player_pos + pygame.Vector2(25, 25)
        drag_vec = pygame.Vector2(pygame.mouse.get_pos()) - press_pos
        drag_dist = min(drag_vec.length(), MAX_DRAG)
        
        # 1. 색상 결정 (강도 10이면 빨강, 아니면 초록)
        guide_color = RED if current_level >= 10 else GREEN
        
        # 2. 가변 원 그리기 (강도에 따라 커지며, 최대 MAX_DRAG까지)
        # 반지름 기본값 40 + 드래그 거리 비례 증가
        guide_radius = 40 + (drag_dist * 0.8) 
        pygame.draw.circle(screen, guide_color, (int(center.x), int(center.y)), int(guide_radius), 2)
        
        # 3. 십자선 (원 내부에 고정)
        pygame.draw.line(screen, guide_color, (center.x - guide_radius, center.y), (center.x + guide_radius, center.y), 1)
        pygame.draw.line(screen, guide_color, (center.x, center.y - guide_radius), (center.x, center.y + guide_radius), 1)

        # 4. 방향 화살표 (원의 경계선 위에 배치)
        if drag_vec.length() > 0:
            aim_dir = -drag_vec.normalize()
            arrow_pos = center + aim_dir * guide_radius
            
            # 화살촉 삼각형 그리기
            wing_l = arrow_pos + aim_dir.rotate(150) * 15
            wing_r = arrow_pos + aim_dir.rotate(-150) * 15
            pygame.draw.polygon(screen, guide_color, [arrow_pos, wing_l, wing_r])

    # 정보 텍스트
    status_msg = f"Power: {current_level} | Enemy: {'MOVING' if enemy_is_moving else 'STOPPED'}"
    screen.blit(font.render(status_msg, True, BLACK if can_move else RED), (20, 20))

    for p in projectiles: p.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()