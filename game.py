import numpy as np
import random
import pygame
import math

class PowderToy:
    def __init__(self):
        # Set display settings
        self.GAMEWIDTH = 1000
        self.WIDTH = 1400
        self.HEIGHT = 1000
        self.RESOLUTION = 10
        self.CELLS_X = self.GAMEWIDTH // self.RESOLUTION
        self.CELLS_Y = self.HEIGHT // self.RESOLUTION
        self.TEXT_CENTRE = self.GAMEWIDTH + ((self.WIDTH - self.GAMEWIDTH) // 2)
        self.FPS = 30

        # Create grid to store game
        self.grid = np.zeros((self.CELLS_Y, self.CELLS_X))
        # Grid to store velocity, with components (y, x)
        self.velocityGrid = np.zeros((self.CELLS_Y, self.CELLS_X, 2))
        # Grid to store colours in use
        self.colourGrid = np.zeros((self.CELLS_Y, self.CELLS_X), dtype=object)

        # Physics constants
        self.GRAVITY = 0.7
        self.TERMINAL_VELOCITY = 3

        # Setup for mouse controls
        self.leftMouseHeld = False
        self.rightMouseHeld = False
        self.currentMaterial = 1

        # Dictionary to hold colour values
        self.colours = {
            "0": [(0, 0, 0)],
            # Sand
            "1": [(117, 108, 30), (156, 113, 28), (181, 128, 22), (153, 126, 20), (140, 114, 13)]
        }

        # Perform initialisation for pygame
        pygame.init()
        pygame.font.init()
        # Define 3 font sizes
        self.fontLarge = pygame.font.SysFont(None, 50)
        self.fontMedium = pygame.font.SysFont(None, 40)
        self.fontSmall = pygame.font.SysFont(None, 29)
        # Set window attributes
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Powder Toy")
        self.clock = pygame.time.Clock()
        self.running = True

        # Create visible grid of 1px border around cells
        self.screen.fill("black")

        # Create menu title
        pygame.draw.line(self.screen, (255, 255, 255), (1000, 0), (1000, 1000), 2)
        title = self.fontLarge.render("Powder Toy", True, (255, 255, 255))
        titleRect = title.get_rect()
        titleRect.center = (self.TEXT_CENTRE, 50)
        self.screen.blit(title, titleRect)

        # Initialize grid with some sand
        self.grid[(self.CELLS_Y // 2) - 50:(self.CELLS_Y // 2) - 20, 0:30] = 1

    # Draws the grid
    def draw_grid(self):
        for i in range(self.CELLS_Y):
            for j in range(self.CELLS_X):
                # Actual positions of the visible grid square
                x = j * self.RESOLUTION
                y = i * self.RESOLUTION

                # Set colour if coloured flag is True
                if self.colourGrid[i, j] == 0 and self.grid[i, j] != 0:
                    colour = self.get_cell_colour(j, i)
                elif self.colourGrid[i, j] != 0:
                    colour = self.colourGrid[i, j]

                if self.grid[i, j] == 1:
                    # Draw at x and y + 1 with Resolution - 2 in order to not hide the grid lines
                    pygame.draw.rect(self.screen, colour, (x, y, self.RESOLUTION, self.RESOLUTION))
                    self.colourGrid[i, j] = colour
                else:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.RESOLUTION, self.RESOLUTION))

    # Gets the colour of the given cell
    def get_cell_colour(self, x, y):
        # Just return sand colour for now
        return random.choice(self.colours[str(int(self.grid[y, x]))])

    # Used to move sand particles
    def move_sand(self, y, x, roi, newGrid):
        # If can't move
        if np.array_equal(roi[2], [1, 1, 1]):
            self.velocityGrid[y, x, 0] = 0
            return newGrid  

        # Update velocity (accelerate)
        self.velocityGrid[y, x, 0] += self.GRAVITY

        # Conform to terminal velocity
        if self.velocityGrid[y, x, 0] > self.TERMINAL_VELOCITY:
            self.velocityGrid[y, x, 0] = self.TERMINAL_VELOCITY

        newY = y + int(self.velocityGrid[y, x, 0])

        if newY >= self.CELLS_Y:
            newY = self.CELLS_Y - 1

        # If can fall straight down
        if y < self.CELLS_Y - 1:
            if roi[2, 1] == 0:
                # Fall as far as velocity allows
                for i in range(newY, y, -1):
                    if i < self.CELLS_Y and newGrid[i, x] == 0:
                        newGrid[i, x] = newGrid[y, x]
                        newGrid[y, x] = 0
                        self.velocityGrid[i, x] = self.velocityGrid[y, x]
                        self.velocityGrid[y, x] = 0
                        self.colourGrid[i, x] = self.colourGrid[y, x]
                        self.colourGrid[y, x] = 0
                        break
            # If can move left
            elif np.array_equal(roi[2], [0, 1, 1]) and x > 0:
                newGrid[y+1, x-1] = newGrid[y, x]
                newGrid[y, x] = 0
                self.velocityGrid[y+1, x-1] = self.velocityGrid[y, x]
                self.velocityGrid[y, x] = 0
                self.colourGrid[y+1, x-1] = self.colourGrid[y, x]
                self.colourGrid[y, x] = 0
            # If can move right
            elif np.array_equal(roi[2], [1, 1, 0]) and x < self.CELLS_X - 1:
                newGrid[y+1, x+1] = newGrid[y, x]
                newGrid[y, x] = 0
                self.velocityGrid[y+1, x+1] = self.velocityGrid[y, x]
                self.velocityGrid[y, x] = 0
                self.colourGrid[y+1, x+1] = self.colourGrid[y, x]
                self.colourGrid[y, x] = 0
            # Stochastic movement if can move either direction
            elif np.array_equal(roi[2], [0, 1, 0]):
                # Cant move right, move left
                if x == self.CELLS_X - 1:
                    newGrid[y+1, x-1] = newGrid[y, x]
                    newGrid[y, x] = 0
                    self.velocityGrid[y+1, x-1] = self.velocityGrid[y, x]
                    self.velocityGrid[y, x] = 0
                    self.colourGrid[y+1, x-1] = self.colourGrid[y, x]
                    self.colourGrid[y, x] = 0
                # Cant move left, move right
                elif x == 0:
                    newGrid[y+1, x+1] = newGrid[y, x]
                    newGrid[y, x] = 0
                    self.velocityGrid[y+1, x+1] = self.velocityGrid[y, x]
                    self.velocityGrid[y, x] = 0
                    self.colourGrid[y+1, x+1] = self.colourGrid[y, x]
                    self.colourGrid[y, x] = 0
                else:
                    direction = random.randint(0, 1)
                    # Move left
                    if direction == 0:
                        newGrid[y+1, x-1] = newGrid[y, x]
                        newGrid[y, x] = 0
                        self.velocityGrid[y+1, x-1] = self.velocityGrid[y, x]
                        self.velocityGrid[y, x] = 0
                        self.colourGrid[y+1, x-1] = self.colourGrid[y, x]
                        self.colourGrid[y, x] = 0
                    # Move right
                    else:
                        newGrid[y+1, x+1] = newGrid[y, x]
                        newGrid[y, x] = 0
                        self.velocityGrid[y+1, x+1] = self.velocityGrid[y, x]
                        self.velocityGrid[y, x] = 0
                        self.colourGrid[y+1, x+1] = self.colourGrid[y, x]
                        self.colourGrid[y, x] = 0

        return newGrid

    # Handles movement of cells
    def move_cells(self):
        newGrid = self.grid.copy()
        paddedGrid = np.pad(newGrid, pad_width=1, mode='constant', constant_values=0)
        for i in range(1, self.CELLS_Y + 1):
            for j in range(1, self.CELLS_X + 1):
                # Get ROI, accounting for corners and edges
                roi = paddedGrid[i-1:i+2, j-1:j+2]

                # If sand
                if roi[1, 1] == 1:
                    newGrid = self.move_sand(i-1, j-1, roi, newGrid)
        
        self.grid = newGrid

    # Handles input events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True  # Pause or unpause the game
                elif event.key == pygame.K_c:
                    self.clear_grid()
                elif event.key == pygame.K_q:
                    self.running = False
                    pygame.quit()

            # Check for mouse button presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.leftMouseHeld = True
                if event.button == 3:
                    self.rightMouseHeld = True
                    
            # Check for mouse button releases
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.leftMouseHeld = False
                if event.button == 3:
                    self.rightMouseHeld = False
        
        return False
    
    # Handles mouse actions
    def handle_mouse_input(self):
        if self.leftMouseHeld:
            x, y = pygame.mouse.get_pos()
            cellX = x // self.RESOLUTION
            cellY = y // self.RESOLUTION
            if cellX < self.CELLS_X and cellY < self.CELLS_Y:
                self.grid[cellY, cellX] = self.currentMaterial

        if self.rightMouseHeld:
            x, y = pygame.mouse.get_pos()
            cellX = x // self.RESOLUTION
            cellY = y // self.RESOLUTION
            if cellX < self.CELLS_X and cellY < self.CELLS_Y:
                self.grid[cellY, cellX] = 0
                self.velocityGrid[cellY, cellX] = 0

    def clear_grid(self):
        self.grid.fill(0)
        self.velocityGrid = np.zeros((self.CELLS_Y, self.CELLS_X, 2))
        self.colourGrid.fill(0)

        self.draw_grid()

    def draw_pause_message(self, message):
        pygame.draw.rect(self.screen, (0, 0, 0), (1010, 110, 1390, 150))
        pauseText = self.fontMedium.render(message, True, (255, 255, 255))
        pauseTextRect = pauseText.get_rect()
        pauseTextRect.center = (1200, 150)
        self.screen.blit(pauseText, pauseTextRect)
        pygame.display.flip()

    def run(self):
        self.draw_pause_message("Game is Running")

        while self.running:

            if self.handle_events():
                self.running = False
                break
            
            self.move_cells()
            self.handle_mouse_input()
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(self.FPS)

        while not self.running:
            self.draw_pause_message("Game is Paused")

            if self.handle_events():
                self.running = True
                self.run()

            self.handle_mouse_input()
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    game = PowderToy()
    game.run()
    pygame.quit()
