from .Particle import Particle
import numpy as np
import pygame
import random


# Holds information about the sand particle
class Sand(Particle):
    def __init__(self, x, y):
        colours = [(117, 108, 30), (156, 113, 28), (181, 128, 22), (153, 126, 20), (140, 114, 13)]
        super().__init__(x, y, random.choice(colours))
        self.ID = 1
        self.NAME = "Sand"
        self.GRAVITY = 0.7
        self.TERMINAL_VELOCITY = 5

    # Used to move sand particles
    def move(self, newGrid, y, x):
        CELLS_Y = len(newGrid)
        CELLS_X = len(newGrid[0])

        # Update velocity (accelerate)
        self.velocity[0] += self.GRAVITY

        # Conform to terminal velocity
        if self.velocity[0] > self.TERMINAL_VELOCITY:
            self.velocity[0] = self.TERMINAL_VELOCITY

        newY = y + int(self.velocity[0])

        if newY >= CELLS_Y:
            newY = CELLS_Y - 1

        # Chech each direction below the particle
        b, bl, br = False, False, False
        if y < CELLS_Y - 1:
            if newGrid[y+1, x] == 0:
                b = True
            if x > 0 and newGrid[y+1, x-1] == 0:
                bl = True
            if x < CELLS_X - 1 and newGrid[y+1, x+1] == 0:
                br = True
        else:
            return newGrid
        
        # If can fall straight down
        if b:
            for i in range(newY, y, -1):
                if newGrid[i, x] == 0:
                    newGrid[i, x] = newGrid[y, x]
                    newGrid[y, x] = 0
                    self.y = i
                    return newGrid
        
        # If can only move left
        if bl and not br:
            newGrid[y+1, x-1] = newGrid[y, x]
            newGrid[y, x] = 0
            self.y += 1
            self.x -=1
            return newGrid
        # If can only move right
        elif br and not bl:
            newGrid[y+1, x+1] = newGrid[y, x]
            newGrid[y, x] = 0
            self.y += 1
            self.x +=1
            return newGrid
        # If can move either direction
        # Random movement
        elif br and bl:
            direction = random.randint(0, 1)
            # Move left
            if direction == 0:
                newGrid[y+1, x-1] = newGrid[y, x]
                newGrid[y, x] = 0
                self.y += 1
                self.x -=1
                return newGrid
            # Move right
            else:
                newGrid[y+1, x+1] = newGrid[y, x]
                newGrid[y, x] = 0
                self.y += 1
                self.x +=1
                return newGrid
        else:
            return newGrid
        