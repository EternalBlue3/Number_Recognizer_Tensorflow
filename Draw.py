import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pygame
from Recognizer import probability_model
from PIL import Image
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
label = FONT.render("Classify", 1, WHITE)

# Define the area for drawing
drawing_area = pygame.Rect(0, 0, canvas_width, canvas_height - 100)  # Adjusted the canvas height for the drawing area

prev_pos = None
curr_pos = None

def recognize(img):
    image = Image.fromarray(img).convert('L').rotate(270)
    image = image.transpose(Image.FLIP_LEFT_RIGHT).resize((28,28))
    
    image = np.array(image)
    image = image.expand_dims(image, axis=-1)  # Add an additional dimension for channel
    image = image.astype('float32') / 255.0  # Normalize the image
    image = np.expand_dims(image, axis=0)
    image = image.reshape(1, 784)  # Reshape the image to (1, 784)
    prediction = probability_model.predict(image)
    prediction = np.argmax(prediction)
    print("Prediction: ", prediction)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                canvas.fill((0,0,0))

    # Get the current mouse position
    curr_pos = pygame.mouse.get_pos()

    # Check if the left mouse button is pressed
    if pygame.mouse.get_pressed()[0]:
        # If there is no previous position, set it to the current position
        if not drawing_area.collidepoint(curr_pos):  # Check if the current position is within the drawing area
            image = pygame.surfarray.array3d(canvas)
            recognize(image[:600, :600, :])  # Crop to 600x600 area
        else:
            if prev_pos is None:
                prev_pos = curr_pos

            # Draw a line from the previous position to the current position
            pygame.draw.line(canvas, WHITE, prev_pos, curr_pos, 25)

            # Interpolate the line between the previous and current positions
            dx = curr_pos[0] - prev_pos[0]
            dy = curr_pos[1] - prev_pos[1]
            distance = max(abs(dx), abs(dy))
            for i in range(1, distance):
                x = prev_pos[0] + int(i * dx / distance)
                y = prev_pos[1] + int(i * dy / distance)
                pygame.draw.circle(canvas, WHITE, (x, y), 25)

            # Update the previous position to the current position
            prev_pos = curr_pos
    else:
        # Reset the previous position when the mouse button is released
        prev_pos = None

    # Draw the button area
    pygame.draw.rect(canvas, GRAY, (0, canvas_height - 100, canvas_width, 100))
    canvas.blit(label, (canvas_width/2 - label.get_width()/2, canvas_height - 75))
    pygame.display.update()

# Quit Pygame
pygame.quit()
