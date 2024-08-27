from particles.Sand import *
from particles.Water import *
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
        self.RESOLUTION = 5
        self.CELLS_X = self.GAMEWIDTH // self.RESOLUTION
        self.CELLS_Y = self.HEIGHT // self.RESOLUTION
        self.TEXT_CENTRE = self.GAMEWIDTH + ((self.WIDTH - self.GAMEWIDTH) // 2)
        self.FPS = 30

        # Create grid to store game
        self.grid = np.zeros((self.CELLS_Y, self.CELLS_X), dtype=object)

        # Setup for mouse controls
        self.leftMouseHeld = False
        self.rightMouseHeld = False
        self.currentMaterial = Water

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
        for i in range(20, 49):
            for j in range(0, 29):
                self.grid[i, j] = Sand(j, i)

        # Initialize grid with some sand
        for i in range(20, 49):
            for j in range(70, 99):
                self.grid[i, j] = Water(j, i)


    # Draws the grid
    def draw_grid(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.GAMEWIDTH, self.HEIGHT))
        for i in range(self.CELLS_Y):
            for j in range(self.CELLS_X):
                # Actual positions of the visible grid square
                x = j * self.RESOLUTION
                y = i * self.RESOLUTION

                if self.grid[i, j] != 0:
                    # Draw at x and y + 1 with Resolution - 2 in order to not hide the grid lines
                    self.grid[i, j].draw(self.screen, self.RESOLUTION)

    # Gets the colour of the given cell
    def get_cell_colour(self, x, y):
        # Just return sand colour for now
        return random.choice(self.colours[str(int(self.grid[y, x]))])

    # Handles movement of cells
    def move_cells(self):
        newGrid = self.grid.copy()
        for i in range(self.CELLS_Y - 1, -1, -1):
            # Get x iteration direction
            if i % 2 == 0:
                rangeJ = range(0, self.CELLS_X)
            else:
                rangeJ = range(self.CELLS_X - 1, -1, -1)

            for j in rangeJ:
                if newGrid[i, j] != 0:
                    newGrid = newGrid[i, j].move(newGrid, i, j)

        
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
            x = x // self.RESOLUTION
            y = y // self.RESOLUTION
            maxY = min(self.CELLS_Y, y + 3)
            minY = max(0, y - 2)
            maxX = min(self.CELLS_X, x + 3)
            minX = max(0, x - 2)
            choices = [self.currentMaterial, 0]
            for i in range(minY, maxY):
                for j in range(minX, maxX):
                    if self.grid[i, j] == 0 and random.choice(choices) != 0:
                        self.grid[i, j] = self.currentMaterial(j, i)

        if self.rightMouseHeld:
            x, y = pygame.mouse.get_pos()
            x = x // self.RESOLUTION
            y = y // self.RESOLUTION
            maxY = min(self.CELLS_Y, y + 3)
            minY = max(0, y - 2)
            maxX = min(self.CELLS_X, x + 3)
            minX = max(0, x - 2)
            for i in range(minY, maxY):
                for j in range(minX, maxX):
                    self.grid[i, j] = 0


    def clear_grid(self):
        self.grid.fill(0)

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

            sand_count = 0
            water_count = 0
            
            # for row in self.grid:
            #     for cell in row:
            #         if isinstance(cell, Sand):
            #             sand_count += 1
            #         elif isinstance(cell, Water):
            #             water_count += 1

            # print(f"sand_count {sand_count}, water_count {water_count}")

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