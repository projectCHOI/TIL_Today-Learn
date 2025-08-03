import pygame

# === 초기 설정 ===
pygame.init()
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
TILE_SIZE = WIDTH // COLS
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Tactics Arena - Training Version")

# 색상
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
# === 유닛 클래스 ===
class Unit:
    def __init__(self, x, y, color, move_range=3, hp=3):
        self.x = x
        self.y = y
        self.color = color
        self.move_range = move_range
        self.hp = hp

    def draw(self, win):
        pygame.draw.circle(
            win,
            self.color,
            (self.x * TILE_SIZE + TILE_SIZE//2, self.y * TILE_SIZE + TILE_SIZE//2),
            TILE_SIZE//3
        )
        # 체력 표시
        font = pygame.font.SysFont(None, 20)
        text = font.render(str(self.hp), True, BLACK)
        win.blit(text, (self.x*TILE_SIZE + TILE_SIZE//3, self.y*TILE_SIZE + TILE_SIZE//3))

    def is_clicked(self, gx, gy):
        return self.x == gx and self.y == gy

# === 초기 유닛 배치 ===
units = [
    Unit(0, 0, BLUE),
    Unit(1, 0, BLUE),
    Unit(9, 9, RED),
    Unit(8, 9, RED)
]

selected = None
turn = "blue"

# === 보드 그리기 ===
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(win, GRAY, rect, 1)

# === 턴 전환 ===
def next_turn():
    global turn, selected
    turn = "red" if turn == "blue" else "blue"
    selected = None

# === 메인 루프 ===
def main():
    global selected
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        win.fill(WHITE)

        draw_grid()
        for u in units:
            u.draw(win)

        # 턴 표시
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"{turn.upper()} TURN", True, BLACK)
        win.blit(text, (10, 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                gx, gy = mx // TILE_SIZE, my // TILE_SIZE

                if selected:
                    # === 공격 (인접한 적 클릭) ===
                    for u in units:
                        if u.is_clicked(gx, gy) and u.color != selected.color:
                            dist = abs(selected.x - u.x) + abs(selected.y - u.y)
                            if dist == 1:  # 인접한 경우만 공격
                                u.hp -= 1
                                if u.hp <= 0:
                                    units.remove(u)
                                next_turn()
                                break
                    else:
                        # === 이동 (빈칸 클릭) ===
                        dist = abs(selected.x - gx) + abs(selected.y - gy)
                        occupied = any(u.is_clicked(gx, gy) for u in units)
                        if dist <= selected.move_range and not occupied:
                            selected.x, selected.y = gx, gy
                            next_turn()
                    selected = None
                else:
                    # === 유닛 선택 ===
                    for u in units:
                        if u.is_clicked(gx, gy) and (
                            (turn == "blue" and u.color == BLUE) or
                            (turn == "red" and u.color == RED)
                        ):
                            selected = u

    pygame.quit()

if __name__ == "__main__":
    main()