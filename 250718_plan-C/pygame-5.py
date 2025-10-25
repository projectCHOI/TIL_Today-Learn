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

    # 줄 길이 일관성
    widths = {len(row) for row in data["map"]}
    if len(widths) != 1:
        raise ValueError(f"[오류] 모든 줄의 길이가 동일해야 합니다: {filename}")

    # legend 없으면 기본값 부여
    if "legend" not in data:
        data["legend"] = {"#": "wall", ".": "floor", "S": "start", "G": "goal"}

    print(f"[로드 완료] {filename} | tile={data['tile']} | rows={len(data['map'])}")
    return data
    
# 맵
def build_stage_from_json(data: dict, screen_w: int, screen_h: int):
    tile   = int(data["tile"])
    grid   = data["map"]
    legend = data["legend"]

    rows = len(grid)
    cols = len(grid[0])

    map_w = cols * tile
    map_h = rows * tile

    off_x = (screen_w - map_w) // 2
    off_y = (screen_h - map_h) // 2

    walls = []
    start_pos = None
    goal_rect = None

    def is_type(ch: str, type_name: str) -> bool:
        return legend.get(ch) == type_name

    for r, line in enumerate(grid):
        for c, ch in enumerate(line):
            x = off_x + c * tile
            y = off_y + r * tile
            rect = pygame.Rect(x, y, tile, tile)

            if is_type(ch, "wall"):
                walls.append(rect)
            elif is_type(ch, "start"):
                start_pos = rect.center
            elif is_type(ch, "goal"):
                goal_rect = rect

    if start_pos is None:
        raise ValueError("[맵 오류] 'start(S)'가 없습니다.")
    if goal_rect is None:
        raise ValueError("[맵 오류] 'goal(G)'이 없습니다.")

    return {
        "name": data.get("name", "Unnamed Stage"),
        "tile": tile,
        "grid": grid,
        "legend": legend,
        "walls": walls,
        "start": start_pos,
        "goal": goal_rect,
        "offset": (off_x, off_y),
        "map_px": (map_w, map_h),
        "size": (cols, rows),
    }

# 유닛
def create_star_surface(size, color):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size / 2, size / 2
    R = size * 0.48
    r = R * 0.5
    pts = []
    start_angle = -math.pi / 2
    for i in range(10):
        ang = start_angle + i * (math.pi / 5)
        radius = R if i % 2 == 0 else r
        x = cx + radius * math.cos(ang)
        y = cy + radius * math.sin(ang)
        pts.append((x, y))
    pygame.draw.polygon(surf, color, pts)
    return surf
    
# 플레이어
class Player:
    def __init__(self, spawn_xy, tile):
        self.size = max(10, int(tile * 0.8))
        self.speed = max(2.0, tile * 0.15)
        self.x, self.y = spawn_xy

        self.base_color = YELLOW
        self.select_color = BLUE
        self.surf_base = create_star_surface(self.size, self.base_color)
        self.surf_select = create_star_surface(self.size, self.select_color)

        self.rotating = False
        self.angle = 0
        self.rotate_ms = 300
        self.rotate_start = 0

    @property
    def rect(self):
        half = self.size / 2
        return pygame.Rect(int(self.x - half), int(self.y - half), self.size, self.size)

    def start_select(self):
        if not self.rotating:
            self.rotating = True
            self.rotate_start = pygame.time.get_ticks()
            self.angle = 0

    def move_and_collide(self, dx, dy, walls):
        self.x += dx
        r = self.rect
        for w in walls:
            if r.colliderect(w):
                if dx > 0:
                    self.x = w.left - r.width / 2
                elif dx < 0:
                    self.x = w.right + r.width / 2
                r = self.rect
        self.y += dy
        r = self.rect
        for w in walls:
            if r.colliderect(w):
                if dy > 0:
                    self.y = w.top - r.height / 2
                elif dy < 0:
                    self.y = w.bottom + r.height / 2
                r = self.rect

    def update(self, dt, keys, walls):
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed * dt
        dy = (keys[pygame.K_DOWN]  - keys[pygame.K_UP])   * self.speed * dt
        self.move_and_collide(dx, dy, walls)

        if self.rotating:
            elapsed = pygame.time.get_ticks() - self.rotate_start
            t = max(0.0, min(1.0, elapsed / self.rotate_ms))
            self.angle = 360 * t
            if t >= 1.0:
                self.rotating = False
                self.angle = 0

    def draw(self, surface):
        src = self.surf_select if self.rotating else self.surf_base
        if self.rotating:
            rotated = pygame.transform.rotate(src, self.angle)
            rect = rotated.get_rect(center=(self.x, self.y))
            surface.blit(rotated, rect.topleft)
        else:
            rect = src.get_rect(center=(self.x, self.y))
            surface.blit(src, rect.topleft)

# 맵
def draw_map(info, surf):
    tile = info["tile"]
    off_x, off_y = info["offset"]
    grid = info["grid"]
    # 바닥(경계)
    pygame.draw.rect(surf, PATH, (off_x, off_y, info["map_px"][0], info["map_px"][1]))

    for r, line in enumerate(grid):
        for c, ch in enumerate(line):
            x = off_x + c * tile
            y = off_y + r * tile
            rect = pygame.Rect(x, y, tile, tile)
            if info["legend"].get(ch) == "wall":
                pygame.draw.rect(surf, WALL, rect)
            elif info["legend"].get(ch) == "start":
                pygame.draw.rect(surf, START, rect, width=2)
            elif info["legend"].get(ch) == "goal":
                pygame.draw.rect(surf, GOAL, rect)

# 스테이지 로드
def find_stage_files():
    if not os.path.exists(MAP_DIR):
        raise FileNotFoundError(f"[오류] 맵 폴더가 없습니다: {MAP_DIR}")
    files = [f for f in os.listdir(MAP_DIR) if f.lower().endswith(".json")]
    files.sort()
    if not files:
        raise FileNotFoundError(f"[오류] JSON 스테이지 파일이 없습니다: {MAP_DIR}")
    return files

# 메인 루프
def main():
    stage_files = find_stage_files()  # 예: ['stage1.json', 'stage2.json', ...]
    stage_idx = 0
    stage_data = load_stage_json(stage_files[stage_idx])
    info = build_stage_from_json(stage_data, WIDTH, HEIGHT)
    player = Player(info["start"], info["tile"])
    running = True