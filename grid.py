import pygame
pygame.init()

def get_grid():
    grids2 = []
    for y in range(28):
        for x in range(28):
            grids2.append(pygame.Rect(20*x, 20*y, 20, 20))
    return grids2

COLORS = [
    # Colors
    pygame.Rect(0, 500, 50, 50), # BLACK
    pygame.Rect(50, 500, 50, 50), # WHITE
    pygame.Rect(100, 500, 50, 50), # YELLOW
    pygame.Rect(150, 500, 50, 50), # ORANGE
    pygame.Rect(200, 500, 50, 50), # RED
    pygame.Rect(250, 500, 50, 50), # PINK
    pygame.Rect(300, 500, 50, 50), # PURPLE
    pygame.Rect(350, 500, 50, 50), # BLUE
    pygame.Rect(400, 500, 50, 50), # GREEN
    pygame.Rect(450, 500, 50, 50), # BROWN
]
