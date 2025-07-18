import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Move the Box")

x, y = 250, 250
width, height = 40, 40
vel = 5

run = True

