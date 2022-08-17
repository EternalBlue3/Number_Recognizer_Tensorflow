# Modules 
import pygame, numpy
from pygame.locals import *
from grid import get_grid
from Recognizer import load_model
import numpy as np

probability_model = load_model()

# Visual drawing app
pygame.init()

# Grid
grids = get_grid()

# Screen
screen_width, screen_height = 560, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Drawing App")
icon = pygame.image.load("icon.png").convert(screen)
pygame.display.set_icon(icon)
FONT = pygame.font.SysFont("comicsans", 25)

# Game Vars
clock = pygame.time.Clock()
FPS = 60
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
WHITE = (255, 255, 255)

def get_image(black):
    out2 = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    out = []
    
    for y in range(28):
        for x in range(28):
            if grids[(28*y+x)] in black:
                out2[y].append(255)
            else:
                out2[y].append(0)

    for x in out2:
        out.append(np.array(x))
    return np.array(out).reshape(1,28,28)

def draw_4(grid,black):
    
    grid0 = pygame.Rect(grid[0]+20,grid[1],20,20)
    grid1 = pygame.Rect(grid[0]-20,grid[1],20,20)
    grid2 = pygame.Rect(grid[0],grid[1]+20,20,20)
    grid3 = pygame.Rect(grid[0],grid[1]-20,20,20)
    
    for x in range(4):
        exec(f"black.append(grid{x})")

# Blit onto screen
def draw(mouse_rect, mouse_press, black):
    screen.fill(WHITE)
    for grid in grids:
        pygame.draw.rect(screen, BLACK, grid, 1) # this draws the grids
        if mouse_rect.colliderect(grid):
            if mouse_press[0]:
                black.append(grid)
                draw_4(grid,black)
    
    for grid in black: # These run through all the lists and check if a color is in a grid 
        pygame.draw.rect(screen, BLACK, grid)

    pygame.draw.rect(screen, GRAY, pygame.Rect(0,560,560,40))
    
    label = FONT.render("Classify",1,WHITE)
    screen.blit(label, (screen_width/2 - label.get_width()/2, 561))
    
    pygame.display.update()

# Gameloop
def main():
    running = True
    black = [] # These lists are used to display a multitude of colors
    
    while running:
        clock.tick(FPS)
        mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1) # This is used to get the mouse position
        mouse_press = pygame.mouse.get_pressed(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_rect.colliderect(pygame.Rect(0,560,560,40)): # These if statements are for changing the color
                    
                    image = get_image(black)

                    prediction = probability_model.predict(image)
                    prediction = numpy.argmax(prediction)
                    print("Prediction: ", prediction)
                    
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    black = []

        draw(mouse_rect, mouse_press, black)

if __name__ == "__main__":
    main()
