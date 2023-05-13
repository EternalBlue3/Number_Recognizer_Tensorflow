import pygame

def get_grid():
    return [pygame.Rect(20*x,20*y,20,20) for x in range(28) for y in range(28)]
