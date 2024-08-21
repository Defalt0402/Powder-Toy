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
# Grid to store velocity, with components (y, x)
velocityGrid = np.zeros((CELLS_Y, CELLS_X, 2))

# Physics constants
GRAVITY = 0.3
TERMINAL_VELOCITY = 5

# Perform initialisation for pygame
pygame.init()
pygame.font.init()
# Define 3 font sizes
fontLarge = pygame.font.SysFont(None, 50)
fontMedium = pygame.font.SysFont(None, 40)
fontSmall = pygame.font.SysFont(None, 29)
# Set window attributes
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Powder Toy")
clock = pygame.time.Clock()
running = True

# Create visible grid of 1px border around cells
screen.fill("black")
def draw_grid():
    global grid
    for i in range(CELLS_Y):
        for j in range(CELLS_X):
            # Actual positions of the visible grid square
            x = j * RESOLUTION
            y = i * RESOLUTION

            # Set colour if coloured flag is True
            colour = get_cell_colour(j, i)

            if grid[i, j] == 1:
                # Draw at x and y + 1 with Resolution - 2 in order to not hide the grid lines
                pygame.draw.rect(screen, colour, (x, y, RESOLUTION, RESOLUTION))
            else:
                pygame.draw.rect(screen, (0, 0, 0) , (x, y, RESOLUTION, RESOLUTION))

# Determine cell colour
def get_cell_colour(x, y):
    # Just return sand colour for now
    return (114, 117, 30)

# Used to move any oject that moves like sand
def move_sand(y, x, roi, newGrid):
    global velocityGrid

    # Update velocity(accellerate)
    velocityGrid[y, x, 0] += GRAVITY

    # Conform to terminal velocity
    if velocityGrid[y, x, 0] > TERMINAL_VELOCITY:
        velocityGrid[y, x, 0] = TERMINAL_VELOCITY

    newY = y + int(velocityGrid[y, x, 0])

    if newY >= CELLS_Y:
        newY = CELLS_Y - 1

    if y < CELLS_Y - 1:
        # If can fall straight down
        if roi[2, 1] == 0:
            for i in range(newY, y, -1):
                if i < CELLS_Y - 1 and newGrid[i, x] == 0:
                    newGrid[i, x] = newGrid[y, x]
                    newGrid[y, x] = 0
                    velocityGrid[i, x] = velocityGrid[y, x]
                    velocityGrid[y, x] = 0
                    break
        # If can fall left
        elif np.array_equal(roi[2], [0, 1, 1]) and x > 0:
            newGrid[y+1, x-1] = newGrid[y, x]
            newGrid[y, x] = 0
            velocityGrid[y+1, x-1] = velocityGrid[y, x]
            velocityGrid[y, x] = 0
        # If can fall right
        elif np.array_equal(roi[2], [1, 1, 0]) and x < CELLS_X - 1:
            newGrid[y+1, x+1] = newGrid[y, x]
            newGrid[y, x] = 0
            velocityGrid[y+1, x+1] = velocityGrid[y, x]
            velocityGrid[y, x] = 0
        # Stochastic movement if the sand can move either left or right
        elif np.array_equal(roi[2], [0, 1, 0]):
            # If can't move right, move left
            if x == CELLS_X - 1:
                newGrid[y+1, x-1] = newGrid[y, x]
                newGrid[y, x] = 0
                velocityGrid[y+1, x-1] = velocityGrid[y, x]
                velocityGrid[y, x] = 0
            # If can't move left, move right
            elif x == 0:
                newGrid[y+1, x+1] = newGrid[y, x]
                newGrid[y, x] = 0
                velocityGrid[y+1, x+1] = velocityGrid[y, x]
                velocityGrid[y, x] = 0
            # Otherwise, random direction
            else:
                direction = random.randint(0, 1)
                # Move left
                if direction == 0:
                    newGrid[y+1, x-1] = newGrid[y, x]
                    newGrid[y, x] = 0
                    velocityGrid[y+1, x-1] = velocityGrid[y, x]
                    velocityGrid[y, x] = 0
                # Move right
                else:
                    newGrid[y+1, x+1] = newGrid[y, x]
                    newGrid[y, x] = 0
                    velocityGrid[y+1, x+1] = velocityGrid[y, x]
                    velocityGrid[y, x] = 0

    return newGrid



# Create menu title
pygame.draw.line(screen, (255, 255, 255), (1000, 0), (1000, 1000), 2)
title = fontLarge.render("Powder Toy", True, (255, 255, 255))
titleRect = title.get_rect()
titleRect.center = (TEXT_CENTRE, 50)
screen.blit(title, titleRect)

grid[(CELLS_Y//2)-5:(CELLS_Y//2)+5, 40:60] = 1



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

        # Update all cells
        newGrid = np.copy(grid)
        paddedGrid = np.pad(grid, pad_width=1, mode='constant', constant_values=0)
        for i in range(1, CELLS_Y + 1):
            for j in range(1, CELLS_X + 1):
                # Get ROI, accounting for corners and edges
                roi = paddedGrid[i-1:i+2, j-1:j+2]

                # If sand
                if roi[1, 1] == 1:
                    newGrid = move_sand(i-1, j-1, roi, newGrid)

        grid = newGrid

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