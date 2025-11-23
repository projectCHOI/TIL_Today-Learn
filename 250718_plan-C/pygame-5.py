import os
import json
import math
import pygame
import re

# === 기본 설정 ===
pygame.init()
WIDTH, HEIGHT = 800, 600
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

# 추가 색상 (코인/열쇠/문)
COIN_COLOR = (255, 215, 0)    # 금색 느낌
KEY_COLOR  = (255, 140, 0)    # 주황색
DOOR_COLOR = (120, 70, 0)     # 갈색(문)

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
ALLOW_UNKNOWN_AS_FLOOR = False

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

    # 추가: 코인 / 열쇠 / 문 리스트
    coins = []
    keys = []
    doors = []

    unknown_warned = False
    for r, line in enumerate(grid):
        for c, ch in enumerate(line):
            x = off_x + c * tile
            y = off_y + r * tile
            rect = pygame.Rect(x, y, tile, tile)

            ch_type = legend.get(ch, None)

            if ch_type is None:
                if ALLOW_UNKNOWN_AS_FLOOR:
                    if not unknown_warned:
                        print(f"[경고] legend에 없는 문자 '{ch}' 발견 → floor로 처리합니다. (r={r}, c={c})")
                        unknown_warned = True
                else:
                    raise ValueError(f"[맵 오류] legend에 없는 문자 '{ch}' 발견 (r={r}, c={c})")
                continue

            if ch_type == "wall":
                walls.append(rect)
            elif ch_type == "start":
                start_pos = rect.center
            elif ch_type == "goal":
                goal_rect = rect
            elif ch_type == "coin":
                coins.append(rect)
            elif ch_type == "key":
                keys.append(rect)
            elif ch_type == "door":
                doors.append(rect)

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

        # 새로 추가된 정보들
        "coins": coins,
        "keys": keys,
        "doors": doors,
        "coins_total": len(coins),
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
        self.speed = max(120.0, tile * 6.0)
        self.x, self.y = spawn_xy

        self.base_color = YELLOW
        self.select_color = BLUE
        self.surf_base = create_star_surface(self.size, self.base_color)
        self.surf_select = create_star_surface(self.size, self.select_color)