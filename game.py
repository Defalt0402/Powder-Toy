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
# Grid to store colours in use
colourGrid = np.zeros((CELLS_Y, CELLS_X), dtype=object)

# Physics constants
GRAVITY = 0.7
TERMINAL_VELOCITY = 3

# Setup for mouse controls
leftMouseHeld = False
rightMouseHeld = False
currentMaterial = 1

# Dictionary to hold colour values
colours = {
    "0": [(0, 0, 0)],
    # Sand
    "1": [(117, 108, 30), (156, 113, 28), (181, 128, 22), (153, 126, 20), (140, 114, 13)]
           }

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
            if colourGrid[i, j] == 0 and grid[i, j] != 0:
                colour = get_cell_colour(j, i)
            elif colourGrid[i, j] != 0:
                colour = colourGrid[i, j]

            if grid[i, j] == 1:
                # Draw at x and y + 1 with Resolution - 2 in order to not hide the grid lines
                pygame.draw.rect(screen, colour, (x, y, RESOLUTION, RESOLUTION))
                colourGrid[i, j] = colour
            else:
                pygame.draw.rect(screen, (0, 0, 0) , (x, y, RESOLUTION, RESOLUTION))

# Determine cell colour
def get_cell_colour(x, y):
    # Just return sand colour for now
    return random.choice(colours[str(int(grid[y, x]))])

# Used to move any oject that moves like sand
def move_sand(y, x, roi, newGrid):
    global velocityGrid, colourGrid

    if np.array_equal(roi[2], [1, 1, 1]):
        velocityGrid[y, x, 0] = 0
        return newGrid  

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
                if i < CELLS_Y and newGrid[i, x] == 0:
                    newGrid[i, x] = newGrid[y, x]
                    newGrid[y, x] = 0
                    velocityGrid[i, x] = velocityGrid[y, x]
                    velocityGrid[y, x] = 0
                    colourGrid[i, x] = colourGrid[y, x]
                    colourGrid[y, x] = 0
                    break
        # If can fall left
        elif np.array_equal(roi[2], [0, 1, 1]) and x > 0:
            newGrid[y+1, x-1] = newGrid[y, x]
            newGrid[y, x] = 0
            velocityGrid[y+1, x-1] = velocityGrid[y, x]
            velocityGrid[y, x] = 0
            colourGrid[y+1, x-1] = colourGrid[y, x]
            colourGrid[y, x] = 0
        # If can fall right
        elif np.array_equal(roi[2], [1, 1, 0]) and x < CELLS_X - 1:
            newGrid[y+1, x+1] = newGrid[y, x]
            newGrid[y, x] = 0
            velocityGrid[y+1, x+1] = velocityGrid[y, x]
            velocityGrid[y, x] = 0
            colourGrid[y+1, x+1] = colourGrid[y, x]
            colourGrid[y, x] = 0
        # Stochastic movement if the sand can move either left or right
        elif np.array_equal(roi[2], [0, 1, 0]):
            # If can't move right, move left
            if x == CELLS_X - 1:
                newGrid[y+1, x-1] = newGrid[y, x]
                newGrid[y, x] = 0
                velocityGrid[y+1, x-1] = velocityGrid[y, x]
                velocityGrid[y, x] = 0
                colourGrid[y+1, x-1] = colourGrid[y, x]
                colourGrid[y, x] = 0
            # If can't move left, move right
            elif x == 0:
                newGrid[y+1, x+1] = newGrid[y, x]
                newGrid[y, x] = 0
                velocityGrid[y+1, x+1] = velocityGrid[y, x]
                velocityGrid[y, x] = 0
                colourGrid[y+1, x+1] = colourGrid[y, x]
                colourGrid[y, x] = 0
            # Otherwise, random direction
            else:
                direction = random.randint(0, 1)
                # Move left
                if direction == 0:
                    newGrid[y+1, x-1] = newGrid[y, x]
                    newGrid[y, x] = 0
                    velocityGrid[y+1, x-1] = velocityGrid[y, x]
                    velocityGrid[y, x] = 0
                    colourGrid[y+1, x-1] = colourGrid[y, x]
                    colourGrid[y, x] = 0
                # Move right
                else:
                    newGrid[y+1, x+1] = newGrid[y, x]
                    newGrid[y, x] = 0
                    velocityGrid[y+1, x+1] = velocityGrid[y, x]
                    velocityGrid[y, x] = 0
                    colourGrid[y+1, x+1] = colourGrid[y, x]
                    colourGrid[y, x] = 0


    return newGrid

def draw_pause_message(message):
    pygame.draw.rect(screen, (0, 0, 0), (1010, 110, 1390, 150))
    pauseText = fontMedium.render(message, True, (255, 255, 255))
    pauseTextRect = pauseText.get_rect()
    pauseTextRect.center = (1200, 150)
    screen.blit(pauseText, pauseTextRect)
    pygame.display.flip()

def handle_events():
    global running, leftMouseHeld, rightMouseHeld
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return True  # Pause or unpause the game
            elif event.key == pygame.K_c:
                clear_grid()
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
            if event.button == 1:
                leftMouseHeld = False
            elif event.button == 3:
                rightMouseHeld = False
                
    return False

def clear_grid():
    global grid, velocityGrid, colourGrid
    grid.fill(0)
    velocityGrid = np.zeros((CELLS_Y, CELLS_X, 2))
    colourGrid.fill(0)

    draw_grid()

# Create menu title
pygame.draw.line(screen, (255, 255, 255), (1000, 0), (1000, 1000), 2)
title = fontLarge.render("Powder Toy", True, (255, 255, 255))
titleRect = title.get_rect()
titleRect.center = (TEXT_CENTRE, 50)
screen.blit(title, titleRect)

grid[(CELLS_Y//2)-50:(CELLS_Y//2)-20, 0:30] = 1

# Main game loop
def game_loop():
    global running, grid, currentMaterial

    # Tell user game is running
    draw_pause_message("Game is Running")

    # Basic game loop
    while running:
        # Polling key events
        if handle_events():
            running = False
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

        # Draw on grid if mouse is being held
        if leftMouseHeld:
            mouseX, mouseY = pygame.mouse.get_pos()
            # If mouse is in bounds
            if mouseX >= 0 and mouseX < GAMEWIDTH and mouseY >= 0 and mouseY < HEIGHT:
                # Translate mouse position to corresponding grid position
                cellX = mouseX // RESOLUTION
                cellY = mouseY // RESOLUTION
                grid[cellY, cellX] = currentMaterial

        # erase from grid if mouse is being held
        if rightMouseHeld:
            mouseX, mouseY = pygame.mouse.get_pos()
            # If mouse is in bounds
            if mouseX >= 0 and mouseX < GAMEWIDTH and mouseY >= 0 and mouseY < HEIGHT:
                cellX = mouseX // RESOLUTION
                cellY = mouseY // RESOLUTION
                grid[cellY, cellX] = 0
                velocityGrid[cellY, cellX, 0] = 0
                velocityGrid[cellY, cellX, 1] = 0
                colourGrid[cellY, cellX] = 0


        draw_grid()

        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60

    # If Game is paused
    while not running:

        # Tell user game is paused
        draw_pause_message("Game is Paused")

        # Polling key events
        if handle_events():
            running = True
            game_loop()

        # Draw on grid if mouse is being held
        if leftMouseHeld:
            mouseX, mouseY = pygame.mouse.get_pos()
            # If mouse is in bounds
            if mouseX >= 0 and mouseX < GAMEWIDTH and mouseY >= 0 and mouseY < HEIGHT:
                # Translate mouse position to corresponding grid position
                cellX = mouseX // RESOLUTION
                cellY = mouseY // RESOLUTION
                grid[cellY, cellX] = currentMaterial

        # erase from grid if mouse is being held
        if rightMouseHeld:
            mouseX, mouseY = pygame.mouse.get_pos()
            # If mouse is in bounds
            if mouseX >= 0 and mouseX < GAMEWIDTH and mouseY >= 0 and mouseY < HEIGHT:
                cellX = mouseX // RESOLUTION
                cellY = mouseY // RESOLUTION
                grid[cellY, cellX] = 0
                velocityGrid[cellY, cellX, 0] = 0
                velocityGrid[cellY, cellX, 1] = 0
                colourGrid[cellY, cellX] = 0

        draw_grid()

        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60

game_loop()