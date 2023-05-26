import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pygame
from Recognizer import probability_model
from PIL import Image, ImageOps
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the canvas
canvas_width = 600
canvas_height = 700
canvas = pygame.display.set_mode((canvas_width, canvas_height))
pygame.display.set_caption("Drawing Application")

clock = pygame.time.Clock()
FPS = 60
FONT = pygame.font.SysFont("comicsans", 25)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
BLACK = (0, 0, 0)
label = FONT.render("Classify", 1, WHITE)

# Create a separate surface for drawing
drawing_surface = pygame.Surface((canvas_width, canvas_height - 100), pygame.SRCALPHA)

prev_pos = None
curr_pos = None

def recognize(img):
    image = Image.fromarray(img).convert('L').rotate(270)
    image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT).resize((28,28))
    image = ImageOps.invert(image)
    
    image = np.array(image).reshape(1,28,28)
    image = image.astype('float32') / 255.0  # Normalize the image
    probabilities = probability_model.predict(image)
    prediction = np.argmax(probabilities)
    print("Prediction: ", prediction)

running = True
while running:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                # Clear the drawing surface
                drawing_surface.fill((0, 0, 0, 0))  # Set the alpha value to 0 to clear the surface

    # Get the current mouse position
    curr_pos = pygame.mouse.get_pos()

    # Check if the left mouse button is pressed
    if pygame.mouse.get_pressed()[0]:
        if not drawing_surface.get_rect().collidepoint(curr_pos):
            image = pygame.surfarray.array3d(canvas)
            recognize(image[:600, :600, :])  # Give AI 600x600 drawing surface
        else:
            if prev_pos is None:
                prev_pos = curr_pos

            # Interpolate the line between the previous and current positions
            dx = curr_pos[0] - prev_pos[0]
            dy = curr_pos[1] - prev_pos[1]
            distance = max(abs(dx), abs(dy))
            for i in range(1, distance):
                x = prev_pos[0] + int(i * dx / distance)
                y = prev_pos[1] + int(i * dy / distance)
                pygame.draw.circle(drawing_surface, (0, 0, 0, 255), (x, y), 35)

            # Update the previous position to the current position
            prev_pos = curr_pos
    else:
        # Reset the previous position when the mouse button is released
        prev_pos = None

    # Draw the canvas with a white background
    canvas.fill(WHITE)

    # Blit the drawing surface onto the canvas
    canvas.blit(drawing_surface, (0, 0))

    # Draw the button area
    pygame.draw.rect(canvas, GRAY, (0, canvas_height - 100, canvas_width, 100))
    canvas.blit(label, (canvas_width // 2 - label.get_width() // 2, canvas_height - 75))

    pygame.display.update()

# Quit Pygame
pygame.quit()