import numpy as np
import random
import pygame
import math

# Set display settings
GAMEWIDTH = 1000
WIDTH = 1400
HEIGHT = 1000
RESOLUTION = 10
CELLS_X = GAMEWIDTH // RESOLUTION
CELLS_Y = HEIGHT // RESOLUTION
TEXT_CENTRE = GAMEWIDTH + ((WIDTH - GAMEWIDTH) // 2)
FPS = 30

# Create grid to store game
grid = np.zeros((CELLS_Y, CELLS_X))

# Perform initialisation for pygame
pygame.init()
pygame.font.init()
# Define 3 font sizes
fontLarge = pygame.font.SysFont(None, 50)
fontMedium = pygame.font.SysFont(None, 40)
fontSmall = pygame.font.SysFont(None, 29)
# Set window attributes
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()
running = True

# Create visible grid of 1px border around cells
screen.fill("black")

def draw_grid():
    global grid, coloured
    for i in range(CELLS_Y):
        for j in range(CELLS_X):
            # Actual positions of the visible grid square
            x = j * RESOLUTION
            y = i * RESOLUTION

            # Set colour if coloured flag is True
            colour = get_cell_colour(j, i)

            if grid[i, j] == 1:
                # Draw at x and y + 1 with Resolution - 2 in order to not hide the grid lines
                pygame.draw.rect(screen, colour, (x+1, y+1, RESOLUTION-2, RESOLUTION-2))
            else:
                pygame.draw.rect(screen, (0, 0, 0) , (x+1, y+1, RESOLUTION-2, RESOLUTION-2))

def get_cell_colour(x, y):
    r = (x * 255) // CELLS_X
    g = (y * 255) // CELLS_Y
    b = 255 - r

    return (r, g, b)

# Create menu title
pygame.draw.line(screen, (255, 255, 255), (1000, 0), (1000, 1000), 2)
title = fontLarge.render("Powder Toy", True, (255, 255, 255))
titleRect = title.get_rect()
titleRect.center = (TEXT_CENTRE, 50)
screen.blit(title, titleRect)

# Main game loop
def game_loop(leftMouseHeld=None, rightMouseHeld=None):
    global running, grid

    # Tell user game is running
    pygame.draw.rect(screen, (0, 0, 0) , (1010, 110, 1390, 150))
    runningText = fontMedium.render("Game is Running", True, (255, 255, 255))
    runningTextRect = runningText.get_rect()
    runningTextRect.center = (1200, 150)
    screen.blit(runningText, runningTextRect)

     # Check if user is holding the mouse down
    if leftMouseHeld == None:
        # Create Flags used for drawing
        leftMouseHeld = False
        rightMouseHeld = False

    # Basic game loop
    while running:
        # Polling key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                    break
                elif event.key == pygame.K_q:
                    running = False
                    pygame.quit()
            
             # Check for mouse button presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    leftMouseHeld = True
                elif event.button == 3:
                    rightMouseHeld = True

            # Check for mouse button releases
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    leftMouseHeld = False
                elif event.button == 3:
                    rightMouseHeld = False

        # Pause game
        if running == False:
            break

        draw_grid()

        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60

    # If Game is paused
    while not running:

        # Tell user game is paused
        pygame.draw.rect(screen, (0, 0, 0) , (1010, 110, 1390, 150))
        runningText = fontMedium.render("Game is Paused", True, (255, 255, 255))
        runningTextRect = runningText.get_rect()
        runningTextRect.center = (1200, 150)
        screen.blit(runningText, runningTextRect)

        # Polling key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = True
                    break
                elif event.key == pygame.K_q:
                    running = False
                    pygame.quit()
            
             # Check for mouse button presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    leftMouseHeld = True
                elif event.button == 3:
                    rightMouseHeld = True

            # Check for mouse button releases
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    leftMouseHeld = False
                elif event.button == 3:
                    rightMouseHeld = False
        
        if running == True:
            game_loop(leftMouseHeld, rightMouseHeld)

        draw_grid()

        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60

game_loop()