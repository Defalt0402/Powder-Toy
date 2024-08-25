import pygame

# Base class for all particles
class Particle:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour
        self.velocity = [0, 0]  # Velocity in [y, x]
        self.ID = 0
        self.NAME = "None"
        self.GRAVITY = 0
        self.TERMINAL_VELOCITY = 0
        self.BUOYANCY = 0
        self.LIQUID = False

    def move(self, grid, velocityGrid):
        # This method will be overridden by subclasses
        pass

    def draw(self, screen, resolution):
        pygame.draw.rect(screen, self.colour, (self.x * resolution, self.y * resolution, resolution, resolution))
