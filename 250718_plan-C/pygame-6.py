import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame-6: Health & Damage System")

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
hp = 5 # 플레이어 체력
invincible_timer = 0 # 무적 시간 타이머
screen_shake_timer = 0 # 화면 흔들림 타이머

# 적 설정
ENEMY_SIZE = 50
ENEMY_SPEED = 2.5
NUM_ENEMIES = 5
enemies = []

def get_random_outside_pos():
    OFFSET = 60 
    side = random.randint(0, 3)
    if side == 0: return pygame.Vector2(random.randint(-OFFSET, WIDTH+OFFSET), -OFFSET)
    elif side == 1: return pygame.Vector2(random.randint(-OFFSET, WIDTH+OFFSET), HEIGHT+OFFSET)
    elif side == 2: return pygame.Vector2(-OFFSET, random.randint(-OFFSET, HEIGHT+OFFSET))
    else: return pygame.Vector2(WIDTH+OFFSET, random.randint(-OFFSET, HEIGHT+OFFSET))

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

    offset = pygame.Vector2(0, 0)
    if current_time < screen_shake_timer:
        offset = pygame.Vector2(random.randint(-5, 5), random.randint(-5, 5))
    
    screen.fill(WHITE)
    
    # 이벤트 처리
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

    if current_time - enemy_move_timer > 2000:
        enemy_is_moving = not enemy_is_moving
        enemy_move_timer = current_time

    player_rect = pygame.Rect(player_pos.x, player_pos.y, PLAYER_SIZE, PLAYER_SIZE)

    for i in range(len(enemies)):
            if enemy_is_moving:
                dir_p = (player_pos + pygame.Vector2(25, 25)) - (enemies[i] + pygame.Vector2(25, 25))
                if dir_p.length() > 0: enemies[i] += dir_p.normalize() * ENEMY_SPEED
            
            # 플레이어와 적 충돌 (무적 상태 아닐 때만)
            enemy_rect = pygame.Rect(enemies[i].x, enemies[i].y, ENEMY_SIZE, ENEMY_SIZE)
            if player_rect.colliderect(enemy_rect) and current_time > invincible_timer:
                hp -= 1
                invincible_timer = current_time + 2000 # 2초 무적
                screen_shake_timer = current_time + 300 # 0.3초 흔들림
                if hp <= 0:
                    print("Game Over!")
                    running = False

    for p in projectiles[:]:
        p.update()
        hit_enemy = False
        for i in range(len(enemies)):
            if p.pos.distance_to(enemies[i] + pygame.Vector2(25, 25)) < 31:
                score += 100 + (p.level * 20)
                enemies[i] = get_random_outside_pos()
                hit_enemy = True
                break
        if hit_enemy: projectiles.remove(p)
        elif not screen.get_rect().collidepoint(p.pos): projectiles.remove(p)

    if current_time > invincible_timer or (current_time // 100) % 2 == 0:
        p_color = BLUE if can_move else DARK_BLUE
        pygame.draw.rect(screen, p_color, (player_pos.x + offset.x, player_pos.y + offset.y, 50, 50))

    for e_pos in enemies:
        pygame.draw.rect(screen, RED, (e_pos.x + offset.x, e_pos.y + offset.y, 50, 50))
        if not enemy_is_moving:
            pygame.draw.rect(screen, BLACK, (e_pos.x + offset.x, e_pos.y + offset.y, 50, 50), 3)

    if dragging:
        center = player_pos + pygame.Vector2(25, 25)
        guide_color = RED if current_level >= 10 else GREEN
        guide_radius = 30 + (drag_dist * 0.3) 
        pygame.draw.circle(screen, guide_color, (int(center.x + offset.x), int(center.y + offset.y)), int(guide_radius), 2)
        aim_dir = -drag_vec.normalize() if drag_vec.length() > 0 else pygame.Vector2(0, -1)
        dash_len, dash_gap = 4, 4
        for i in range(int(guide_radius / (dash_len + dash_gap))):
            d_start = center + aim_dir * (i * (dash_len + dash_gap))
            d_end = d_start + aim_dir * dash_len
            pygame.draw.line(screen, guide_color, d_start + offset, d_end + offset, 2)
        arrow_pos = center + aim_dir * guide_radius
        wing_l = arrow_pos + aim_dir.rotate(150) * 10
        wing_r = arrow_pos + aim_dir.rotate(-150) * 10
        pygame.draw.polygon(screen, guide_color, [arrow_pos + offset, wing_l + offset, wing_r + offset])
