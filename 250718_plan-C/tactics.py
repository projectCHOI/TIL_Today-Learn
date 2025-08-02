import pygame
pygame.init()
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
TILE_SIZE = WIDTH // COLS
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Tactics Arena")

# 색상
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class Unit:
    def __init__(self, x, y, color, move_range=3):
        self.x = x
        self.y = y
        self.color = color
        self.move_range = move_range

    def draw(self, win):
        pygame.draw.circle(
            win,
            self.color,
            (self.x * TILE_SIZE + TILE_SIZE//2, self.y * TILE_SIZE + TILE_SIZE//2),
            TILE_SIZE//3
        )

units = [
    Unit(0, 0, BLUE),
    Unit(9, 9, RED)
]

selected = None
turn = "blue"

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(win, GRAY, rect, 1)


def main():
    global selected, turn
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        win.fill(WHITE)

        draw_grid()
        for u in units:
            u.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                gx, gy = mx // TILE_SIZE, my // TILE_SIZE

                if selected:
                    # 이동 범위 제한
                    dist = abs(selected.x - gx) + abs(selected.y - gy)
                    if dist <= selected.move_range:
                        selected.x, selected.y = gx, gy
                        selected = None
                        turn = "red" if turn == "blue" else "blue"
                else:
                    # 유닛 선택
                    for u in units:
                        if u.x == gx and u.y == gy and (
                            (turn == "blue" and u.color == BLUE) or
                            (turn == "red" and u.color == RED)
                        ):
                            selected = u

    pygame.quit()

if __name__ == "__main__":
    main()