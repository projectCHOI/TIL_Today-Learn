import os
import json
import math
import pygame

# === 기본 설정 ===
pygame.init()
WIDTH, HEIGHT = 640, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("미로 탐험형 - JSON 스테이지 로더")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WALL  = (35, 35, 35)
PATH  = (230, 230, 230)
GOAL  = (70, 170, 255)
START = (255, 200, 0)
YELLOW = (255, 244, 79)
BLUE   = (0, 120, 255)

FPS = 60
clock = pygame.time.Clock()

# 경로
BASE_DIR = os.path.dirname(__file__)
MAP_DIR  = os.path.join(BASE_DIR, "pygame_maps")

# 폰트
FONT_PATH = r"C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\Open Font License\서평원 꺾깎체\TTF\SLEIGothicTTF.ttf"
try:
    ui_font = pygame.font.Font(FONT_PATH, 18)
except Exception:
    ui_font = pygame.font.SysFont(None, 18)

# JSON 로더
def load_stage_json(filename: str) -> dict:
    path = os.path.join(MAP_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"[오류] 스테이지 파일을 찾을 수 없습니다: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 필수 키
    if "tile" not in data:
        raise ValueError(f"[오류] 'tile' 키가 없습니다: {filename}")
    if "map" not in data:
        raise ValueError(f"[오류] 'map' 키가 없습니다: {filename}")
    
# 맵
def load_stage_json(filename):
    path = os.path.join(MAP_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"[오류] 스테이지 파일을 찾을 수 없습니다: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 기본 키 검증
    required_keys = ["tile", "map"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"[오류] JSON에 '{key}' 항목이 없습니다: {filename}")

    print(f"[로드 완료] {filename} | 타일 크기: {data['tile']}px, 줄 수: {len(data['map'])}")
    return data

if __name__ == "__main__":
    stage_data = load_stage_json("stage1.json")

    # 로드 확인용 출력
    print("스테이지 이름:", stage_data.get("name", "이름 없음"))
    print("타일 크기:", stage_data["tile"])
    print("첫 번째 줄:", stage_data["map"][0])

# 유닛
def create_star_surface(size, color):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size / 2, size / 2
    R = size * 0.48       # 바깥 반지름
    r = R * 0.5           # 안쪽 반지름
    points = []
    # 꼭대기가 위를 향하도록 -90도(= -pi/2)에서 시작
    start_angle = -math.pi / 2
    for i in range(10):
        ang = start_angle + i * (math.pi / 5)  # 36도 간격
        radius = R if i % 2 == 0 else r
        x = cx + radius * math.cos(ang)
        y = cy + radius * math.sin(ang)
        points.append((x, y))
    pygame.draw.polygon(surf, color, points)
    return surf

# 플레이어
class Player:
    def __init__(self, x, y, size=50, speed=4):
        self.size = size
        self.speed = speed
        self.base_color = YELLOW
        self.select_color = BLUE
        # 기본/선택 상태 별 Surface
        self.surf_base = create_star_surface(self.size, self.base_color)
        self.surf_select = create_star_surface(self.size, self.select_color)
        # 위치는 중심 좌표로 관리
        self.x = x
        self.y = y
        # 회전 애니메이션 상태
        self.rotating = False
        self.angle = 0
        self.rotate_ms = 400  # 애니메이션 총 길이(ms)
        self.rotate_start_time = 0

    def start_select_animation(self):
        if not self.rotating:
            self.rotating = True
            self.rotate_start_time = pygame.time.get_ticks()
            self.angle = 0

    def update(self, dt, keys):
        # 이동 (화살표)
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed
        self.x += dx
        self.y += dy
        # 화면 경계 클램프 (별의 크기 고려: 기본 정사각 50 기준)
        half = self.size / 2
        self.x = max(half, min(WIDTH - half, self.x))
        self.y = max(half, min(HEIGHT - half, self.y))
        # 회전 애니메이션 진행
        if self.rotating:
            elapsed = pygame.time.get_ticks() - self.rotate_start_time
            t = max(0.0, min(1.0, elapsed / self.rotate_ms))
            self.angle = 360 * t
            if t >= 1.0:
                self.rotating = False
                self.angle = 0

    def draw(self, surface):
        if self.rotating:
            # 선택 상태(파란 별)로 회전
            src = self.surf_select
        else:
            src = self.surf_base
        if self.rotating:
            rotated = pygame.transform.rotate(src, self.angle)
            rect = rotated.get_rect(center=(self.x, self.y))
            surface.blit(rotated, rect.topleft)
        else:
            rect = src.get_rect(center=(self.x, self.y))
            surface.blit(src, rect.topleft)

def main():
    player = Player(WIDTH/2, HEIGHT/2, size=50, speed=4)
    running = True
    try:
        font = pygame.font.Font(FONT_PATH, 24)
    except:
        print("폰트 에러")
        font = pygame.font.SysFont(None, 24)
    while running:
        dt = CLOCK.tick(FPS)  # ms
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.start_select_animation()

        keys = pygame.key.get_pressed()
        player.update(dt, keys)

        # 그리기
        win.fill(WHITE)
        player.draw(win)

        text = "이동 : ←↑↓→ | 선택 : 스페이스"
        text_surface = font.render(text, True, (0, 0, 0))
        win.blit(text_surface, (20, 20))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()