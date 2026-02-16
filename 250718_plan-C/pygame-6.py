import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame-6: Archery System")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
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

# 플레이어 & 적 설정
PLAYER_SIZE = 50
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

# 점수 및 게임 변수
score = 0
MAX_DRAG = 200 # 드래그 최대치 정의
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
            if drag_vec.length() > 20: # 최소 드래그 거리
                if drag_vec.length() > MAX_DRAG: drag_vec = drag_vec.normalize() * MAX_DRAG
                level = max(0, min(int(drag_vec.length() / (MAX_DRAG/10)), 10))
                speed = [0, 0, 8, 10, 12, 14, 16, 18, 20, 22, 25][level]
                projectiles.append(Projectile(player_pos + pygame.Vector2(25, 25), -drag_vec.normalize() * speed, level))

    # 이동 및 패널티 로직
    current_level = 0
    can_move = True
    if dragging:
        drag_vec = pygame.Vector2(pygame.mouse.get_pos()) - press_pos
        if drag_vec.length() > MAX_DRAG: drag_vec = drag_vec.normalize() * MAX_DRAG
        current_level = int(drag_vec.length() / (MAX_DRAG/10))
        if current_level >= 10: can_move = False

    if can_move:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player_pos.y -= 5
        if keys[pygame.K_s]: player_pos.y += 5
        if keys[pygame.K_a]: player_pos.x -= 5
        if keys[pygame.K_d]: player_pos.x += 5
    
    # 적 AI 및 충돌
    if current_time - enemy_move_timer > 2000:
        enemy_is_moving = not enemy_is_moving
        enemy_move_timer = current_time
    if enemy_is_moving:
        dir_p = (player_pos + pygame.Vector2(25, 25)) - (enemy_pos + pygame.Vector2(25, 25))
        if dir_p.length() > 0: enemy_pos += dir_p.normalize() * ENEMY_SPEED

    for p in projectiles[:]:
        p.update()
        if p.pos.distance_to(enemy_pos + pygame.Vector2(25, 25)) < 31:
            score += 100 + (p.level * 20)
            projectiles.remove(p)
            enemy_pos = get_random_outside_pos()
        elif not screen.get_rect().collidepoint(p.pos): projectiles.remove(p)

    # --- 시각 효과: 화살 조준선 & 활시위 ---
    if dragging:
        center = player_pos + pygame.Vector2(25, 25)
        aim_dir = -drag_vec.normalize() if drag_vec.length() > 0 else pygame.Vector2(0, -1)
        aim_end = center + aim_dir * drag_vec.length()
        
        # 1. 활 몸체 (활시위 보조선) - 반원 형태로 그리기
        bow_color = (100, 50, 0) # 나무색
        tension_color = (255, 0, 0) if not can_move else BLACK
        # 활의 양 끝점 계산 (조준 방향의 수직 방향)
        perp_vec = pygame.Vector2(-aim_dir.y, aim_dir.x) * 30
        bow_start = center + aim_dir * 10 + perp_vec
        bow_end = center + aim_dir * 10 - perp_vec
        
        # 활시위 당기기 (삼각형 형태의 시위)
        pygame.draw.line(screen, GRAY, bow_start, pygame.mouse.get_pos(), 1)
        pygame.draw.line(screen, GRAY, bow_end, pygame.mouse.get_pos(), 1)
        pygame.draw.line(screen, bow_color, bow_start, bow_end, 4) # 활 몸체

        # 2. 화살 조준선 및 화살촉
        pygame.draw.line(screen, tension_color, center, aim_end, 2)
        if drag_vec.length() > 20:
            wing_l = aim_end + aim_dir.rotate(150) * 15
            wing_r = aim_end + aim_dir.rotate(-150) * 15
            pygame.draw.polygon(screen, tension_color, [aim_end, wing_l, wing_r])

    # 그리기 마무리
    pygame.draw.rect(screen, BLUE if can_move else DARK_BLUE, (player_pos.x, player_pos.y, 50, 50))
    pygame.draw.rect(screen, RED, (enemy_pos.x, enemy_pos.y, 50, 50))
    if not enemy_is_moving: pygame.draw.rect(screen, BLACK, (enemy_pos.x, enemy_pos.y, 50, 50), 3)
    
    screen.blit(score_font.render(f"SCORE: {score}", True, BLACK), (WIDTH - 250, 20))
    for p in projectiles: p.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()