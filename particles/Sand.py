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
    def move(self, newGrid, y, x, roi):
        CELLS_Y = len(newGrid)
        CELLS_X = len(newGrid[0])

        # If can't move
        if np.all(roi[2] != 0):
            self.velocity[0] = 0
            return newGrid

        # Update velocity (accelerate)
        self.velocity[0] += self.GRAVITY

        # Conform to terminal velocity
        if self.velocity[0] > self.TERMINAL_VELOCITY:
            self.velocity[0] = self.TERMINAL_VELOCITY

        newY = y + int(self.velocity[0])

        if newY >= CELLS_Y:
            newY = CELLS_Y - 1

        # If can fall straight down
        if y < CELLS_Y - 1:
            if roi[2, 1] == 0:
                # Fall as far as velocity allows
                for i in range(newY, y, -1):
                    if i < CELLS_Y and newGrid[i, x] == 0:
                        newGrid[i, x] = newGrid[y, x]
                        newGrid[y, x] = 0
                        self.y = i
                        return newGrid

                
            # If can move left
            elif roi[2, 0] == 0 and roi[2, 2] != 0 and x > 0:
                if newGrid[y+1, x-1] == 0:
                    newGrid[y+1, x-1] = newGrid[y, x]
                    newGrid[y, x] = 0
                    self.y += 1
                    self.x -=1
            # If can move right
            elif roi[2, 2] == 0 and roi[2, 0] != 0 and x < CELLS_X - 1:
                if newGrid[y+1, x+1] == 0:
                    newGrid[y+1, x+1] = newGrid[y, x]
                    newGrid[y, x] = 0
                    self.y += 1
                    self.x += 1
            # Stochastic movement if can move either direction
            elif roi[2, 2] == 0 and roi[2, 0] == 0 :
                # Cant move right, move left
                if x == CELLS_X - 1:
                    if newGrid[y+1, x-1] == 0:
                        newGrid[y+1, x-1] = newGrid[y, x]
                        newGrid[y, x] = 0
                        self.y += 1
                        self.x -= 1
                # Cant move left, move right
                elif x == 0:
                    if newGrid[y+1, x+1] == 0:
                        newGrid[y+1, x+1] = newGrid[y, x]
                        newGrid[y, x] = 0
                        self.y += 1
                        self.x += 1
                else:
                    direction = random.randint(0, 1)
                    # Move left
                    if direction == 0:
                        if newGrid[y+1, x-1] == 0:
                            newGrid[y+1, x-1] = newGrid[y, x]
                            newGrid[y, x] = 0
                            self.y += 1
                            self.x -= 1
                    # Move right
                    else:
                        if newGrid[y+1, x+1] == 0:
                            newGrid[y+1, x+1] = newGrid[y, x]
                            newGrid[y, x] = 0
                            self.y += 1
                            self.x += 1

        return newGrid
        