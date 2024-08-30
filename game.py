from particles.Sand import *
from particles.Water import *
from Button import *
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
        self.RESOLUTION = 8
        self.CELLS_X = self.GAMEWIDTH // self.RESOLUTION
        self.CELLS_Y = self.HEIGHT // self.RESOLUTION
        self.TEXT_CENTRE = self.GAMEWIDTH + ((self.WIDTH - self.GAMEWIDTH) // 2)
        self.FPS = 30

        # Create grid to store game
        self.grid = np.zeros((self.CELLS_Y, self.CELLS_X), dtype=object)

        # Setup for mouse controls
        self.leftMouseHeld = False
        self.rightMouseHeld = False
        self.currentMaterial = Sand
        self.drawSize = 4

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

        # Create Controls title
        materialTitle = self.fontMedium.render("Controls:", True, (255, 255, 255))
        materialTitleRect = materialTitle.get_rect()
        materialTitleRect.center = (self.TEXT_CENTRE, 230)
        self.screen.blit(materialTitle, materialTitleRect)

        # Controls info text
        pauseText = self.fontSmall.render("To pause and unpause, press:  Space", True, (255, 255, 255))
        clearText = self.fontSmall.render("To clear the grid, press:  C", True, (255, 255, 255))
        drawText = self.fontSmall.render("To draw on the grid, left click on a cell", True, (255, 255, 255))
        eraseText = self.fontSmall.render("To erase from the grid, right click on a cell", True, (255, 255, 255))
        increaseText = self.fontSmall.render("To increase drawing size, press:  ]", True, (255, 255, 255))
        decreaseText = self.fontSmall.render("To decrease drawing size, press:  [", True, (255, 255, 255))
        drawSizeText = self.fontMedium.render(f"Current pen size: {self.drawSize}", True, (255, 255, 255))

        pauseRect = pauseText.get_rect()
        pauseRect.center = (self.TEXT_CENTRE, 265)
        self.screen.blit(pauseText, pauseRect)

        clearRect = clearText.get_rect()
        clearRect.center = (self.TEXT_CENTRE, 295)
        self.screen.blit(clearText, clearRect)

        drawRect = drawText.get_rect()
        drawRect.center = (self.TEXT_CENTRE, 325)
        self.screen.blit(drawText, drawRect)

        eraseRect = eraseText.get_rect()
        eraseRect.center = (self.TEXT_CENTRE, 355)
        self.screen.blit(eraseText, eraseRect)

        increaseRect = increaseText.get_rect()
        increaseRect.center = (self.TEXT_CENTRE, 385)
        self.screen.blit(increaseText, increaseRect)

        decreaseRect = decreaseText.get_rect()
        decreaseRect.center = (self.TEXT_CENTRE, 415)
        self.screen.blit(decreaseText, decreaseRect)

        drawSizeRect = drawSizeText.get_rect()
        drawSizeRect.center = (self.TEXT_CENTRE, 480)
        self.screen.blit(drawSizeText, drawSizeRect)


        # Create materials title
        materialTitle = self.fontMedium.render("Materials:", True, (255, 255, 255))
        materialTitleRect = materialTitle.get_rect()
        materialTitleRect.center = (self.TEXT_CENTRE, 550)
        self.screen.blit(materialTitle, materialTitleRect)


        # Create iteraction buttons
        self.buttons = []
        self.currentButton = 0
        # x, y, width, height, id, text, action
        sandButton = Button(1050, 600, 70, 30, 0, "Sand", action=Sand)
        self.buttons.append(sandButton)
        waterButton = Button(1050, 650, 70, 30, 1, "Water", action=Water)
        self.buttons.append(waterButton)

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

        # Check for brackets seperately to allow for continuous value changing
        keys = pygame.key.get_pressed()

        # Check if the right bracket key is held down
        if keys[pygame.K_RIGHTBRACKET]:
            self.drawSize += 1

        # Check if the left bracket key is held down
        if keys[pygame.K_LEFTBRACKET]:
            self.drawSize -= 1
            if self.drawSize < 0:
                self.drawSize = 0
        
        return False
    
    # Handles mouse actions
    def handle_mouse_input(self):
        if self.leftMouseHeld:
            x, y = pygame.mouse.get_pos()
            x = x // self.RESOLUTION
            y = y // self.RESOLUTION
            width = self.drawSize // 2
            maxY = min(self.CELLS_Y, y + width + 1)
            minY = max(0, y - width)
            maxX = min(self.CELLS_X, x + width + 1)
            minX = max(0, x - width)
            choices = [self.currentMaterial, 0]
            for i in range(minY, maxY):
                for j in range(minX, maxX):
                    if self.grid[i, j] == 0 and random.choice(choices) != 0:
                        self.grid[i, j] = self.currentMaterial(j, i)

        if self.rightMouseHeld:
            x, y = pygame.mouse.get_pos()
            x = x // self.RESOLUTION
            y = y // self.RESOLUTION
            width = self.drawSize // 2
            maxY = min(self.CELLS_Y, y + width + 1)
            minY = max(0, y - width)
            maxX = min(self.CELLS_X, x + width + 1)
            minX = max(0, x - width)
            for i in range(minY, maxY):
                for j in range(minX, maxX):
                    self.grid[i, j] = 0


    def clear_grid(self):
        self.grid.fill(0)

        self.draw_grid()

    # Draws pause status message
    def draw_pause_message(self, message):
        pygame.draw.rect(self.screen, (0, 0, 0), (1010, 110, 400, 100))
        pauseText = self.fontMedium.render(message, True, (255, 255, 255))
        pauseTextRect = pauseText.get_rect()
        pauseTextRect.center = (1200, 150)
        self.screen.blit(pauseText, pauseTextRect)

    # Draws pen size status message
    def update_drawsize_text(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (1010, 450, 400, 50))
        drawSizeText = self.fontMedium.render(f"Current pen size: {self.drawSize}", True, (255, 255, 255))
        drawSizeRect = drawSizeText.get_rect()
        drawSizeRect.center = (self.TEXT_CENTRE, 480)
        self.screen.blit(drawSizeText, drawSizeRect)

    # Used to check which button is pressed/active
    def check_buttons(self):
        for button in self.buttons:
            button.update(self.leftMouseHeld, self.currentButton)
            if button.is_clicked():
                self.currentMaterial = button.get_action()
                self.currentButton = button.id
            button.draw(self.screen)

    def run(self):
        self.draw_pause_message("Game is Running")

        while self.running:

            if self.handle_events():
                self.running = False
                break
            
            self.move_cells()
            self.handle_mouse_input()
            self.update_drawsize_text()
            self.draw_grid()
            self.check_buttons()

            pygame.display.flip()
            self.clock.tick(self.FPS)

        while not self.running:
            self.draw_pause_message("Game is Paused")

            if self.handle_events():
                self.running = True
                self.run()

            self.update_drawsize_text()

            self.handle_mouse_input()
            self.draw_grid()
            self.check_buttons()
            pygame.display.flip()
            self.clock.tick(self.FPS)

        


if __name__ == "__main__":
    game = PowderToy()
    game.run()
    pygame.quit()