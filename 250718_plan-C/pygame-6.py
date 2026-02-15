import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame-6: Spawn from Outside")

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

# 플레이어 설정
PLAYER_SIZE = 50
PLAYER_SPEED = 5
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

# 적(Target) 관련 설정 및 함수
ENEMY_SIZE = 50
ENEMY_SPEED = 3

def get_outside_spawn_pos():
    """화면 밖 사방 중 한 곳의 랜덤 좌표를 반환"""
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':
        return pygame.Vector2(random.randint(0, WIDTH - ENEMY_SIZE), -ENEMY_SIZE)
    elif side == 'bottom':
        return pygame.Vector2(random.randint(0, WIDTH - ENEMY_SIZE), HEIGHT)
    elif side == 'left':
        return pygame.Vector2(-ENEMY_SIZE, random.randint(0, HEIGHT - ENEMY_SIZE))
    elif side == 'right':
        return pygame.Vector2(WIDTH, random.randint(0, HEIGHT - ENEMY_SIZE))

enemy_pos = get_outside_spawn_pos()
enemy_move_timer = pygame.time.get_ticks()
enemy_is_moving = True

# 점수 및 상태 변수
score = 0
last_hit_score = 0
hit_effect_timer = 0
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
        pygame.draw.circle(screen, BLUE, self.pos, 6)

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
            release_pos = pygame.Vector2(pygame.mouse.get_pos())
            drag_vec = release_pos - press_pos
            
            if drag_vec.length() > 0:
                if drag_vec.length() > 200: drag_vec = drag_vec.normalize() * 200
                level = max(0, min(int(drag_vec.length() / 20), 10))
                if level >= 2:
                    speed = [0, 0, 8, 10, 12, 14, 16, 18, 20, 22, 25][level]
                    projectiles.append(Projectile(player_pos + pygame.Vector2(25, 25), -drag_vec.normalize() * speed, level))

    # --- 2. 플레이어 이동 ---
    can_move = True
    if dragging:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        current_level = min(int((mouse_pos - press_pos).length() / 20), 10)
        if current_level >= 10: can_move = False

    if can_move:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player_pos.y -= PLAYER_SPEED
        if keys[pygame.K_s]: player_pos.y += PLAYER_SPEED
        if keys[pygame.K_a]: player_pos.x -= PLAYER_SPEED
        if keys[pygame.K_d]: player_pos.x += PLAYER_SPEED
    
    player_pos.x = max(0, min(player_pos.x, WIDTH - 50))
    player_pos.y = max(0, min(player_pos.y, HEIGHT - 50))

    # --- 3. 적 AI (외부에서 진입) ---
    if current_time - enemy_move_timer > 2000:
        enemy_is_moving = not enemy_is_moving
        enemy_move_timer = current_time

    if enemy_is_moving:
        dir_to_player = (player_pos + pygame.Vector2(25, 25)) - (enemy_pos + pygame.Vector2(25, 25))
        if dir_to_player.length() > 0:
            enemy_pos += dir_to_player.normalize() * ENEMY_SPEED

    # --- 4. 업데이트 및 충돌 ---
    for p in projectiles[:]:
        p.update()
        if p.pos.distance_to(enemy_pos + pygame.Vector2(25, 25)) < (25 + 6):
            gain = 100 + (p.level * 20)
            score += gain
            last_hit_score, hit_effect_timer = gain, current_time
            projectiles.remove(p)
            # 맞으면 다시 화면 밖에서 스폰
            enemy_pos = get_outside_spawn_pos()

        elif p.pos.x < 0 or p.pos.x > WIDTH or p.pos.y < 0 or p.pos.y > HEIGHT:
            projectiles.remove(p)

    # --- 5. 화면 그리기 ---
    screen.fill(WHITE)
    screen.blit(score_font.render(f"SCORE: {score}", True, BLACK), (WIDTH - 250, 20))

    if current_time - hit_effect_timer < 500:
        screen.blit(font.render(f"+{last_hit_score}!", True, RED), (enemy_pos.x, enemy_pos.y - 30))

    pygame.draw.rect(screen, BLUE if can_move else DARK_BLUE, (player_pos.x, player_pos.y, 50, 50))
    pygame.draw.rect(screen, RED, (enemy_pos.x, enemy_pos.y, 50, 50))
    if not enemy_is_moving: pygame.draw.rect(screen, BLACK, (enemy_pos.x, enemy_pos.y, 50, 50), 3)

    if dragging:
            center = player_pos + pygame.Vector2(25, 25)
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            drag_vec = mouse_pos - press_pos
            if drag_vec.length() > MAX_DRAG:
                drag_vec = drag_vec.normalize() * MAX_DRAG
            
            # 1. 파워에 따른 색상 변화 (파랑 -> 빨강)
            power_ratio = drag_vec.length() / MAX_DRAG
            line_color = (int(255 * power_ratio), int(100 * (1 - power_ratio)), int(255 * (1 - power_ratio)))
            
            # 2. 메인 조준선 (화살 몸통)
            aim_end = center - drag_vec
            pygame.draw.line(screen, line_color, center, aim_end, 3)
            
            # 3. 화살촉 그리기 (삼각형)
            if drag_vec.length() > 10:
                arrow_dir = -drag_vec.normalize()
                wing_length = 15
                left_wing = aim_end + arrow_dir.rotate(150) * wing_length
                right_wing = aim_end + arrow_dir.rotate(-150) * wing_length
                
                pygame.draw.polygon(screen, line_color, [aim_end, left_wing, right_wing])

    screen.blit(font.render(f"Power: {current_level} | Enemy: {'MOVING' if enemy_is_moving else 'STOPPED'}", True, BLACK if can_move else RED), (20, 20))
    for p in projectiles: p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()