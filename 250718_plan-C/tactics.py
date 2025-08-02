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
    pygame.quit()

if __name__ == "__main__":
    main()