# Modules 
import pygame, numpy as np, json
from pygame.locals import *
from grid import get_grid

# Visual drawing app
pygame.init()
grids = get_grid()
screen_width, screen_height = 560, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and font
pygame.display.set_caption("Drawing App")
FONT = pygame.font.SysFont("comicsans", 12)

# Game Vars
clock = pygame.time.Clock()
FPS = 60
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
WHITE = (255, 255, 255)

def get_image(black, width=28, height=28):
    out = np.zeros((height, width), dtype=np.uint8)
    
    for grid in black:
        x, y = grid[0] // 20, grid[1] // 20
        if y > 27 or x > 27:
            continue
        else:
            out[y, x] = 255

    out = [out[y, :] for y in range(height)]
    return np.array(out).reshape(1, height, width)

def draw4(grid, black):
    x, y = grid[0], grid[1]
    for dx, dy in [(20, 0), (-20, 0), (0, 20), (0, -20)]:
        black.append(pygame.Rect(x + dx, y + dy, 20, 20))

# Blit onto screen
def draw(mouse_rect, mouse_press, black):
    screen.fill(WHITE)
    
    for grid in grids:
        pygame.draw.rect(screen, BLACK, grid, 1) # this draws the grids
        if mouse_rect.colliderect(grid):
            if mouse_press[0]:
                black.append(grid)
                draw4(grid,black)
    
    for grid in black: # These run through all the lists and check if a color is in a grid 
        pygame.draw.rect(screen, BLACK, grid)
    
    for x in range(10):
        pygame.draw.rect(screen, (10,100,x*15), pygame.Rect(56*x,560,56,40))
        label = FONT.render(str(x),1,WHITE)
        screen.blit(label, ((56*(x+1) - 28) - label.get_width()/2, 580 - label.get_height()/2))
    
    pygame.display.update()
    
def get_classification(mouse_rect):
    for x in range(10):
        if mouse_rect.colliderect(pygame.Rect(56*x,560,56,40)):
            return x

# Gameloop
def main():
    running = True
    black = []
    image_nums = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0}
    
    try:
        with open('stats.txt','r') as fh:
            image_nums = json.loads(fh.read())
    except:
        with open('stats.txt','w') as fh:
            fh.write(json.dumps(image_nums))
    
    while running:
        clock.tick(FPS)
        mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1) # This is used to get the mouse position
        mouse_press = pygame.mouse.get_pressed(3)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                with open('stats.txt','w') as fh:
                    fh.write(json.dumps(image_nums))
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_rect.colliderect(pygame.Rect(0,560,560,40)):
                    classification = get_classification(mouse_rect)
                    image_array = get_image(black)
                    dict_ = image_nums[str(classification)]
                    
                    print("Saving:")
                    print(f"data/{str(classification)}/image_{dict_}.npy")
                    
                    np.save(f"data/{str(classification)}/image_{dict_}.npy", image_array)
                    image_nums[str(classification)] = dict_ + 1
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    black = []

        draw(mouse_rect, mouse_press, black)

if __name__ == "__main__":
    main()