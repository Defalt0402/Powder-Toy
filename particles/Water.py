from .Particle import Particle
import numpy as np
import pygame
import random


# Holds information about the sand particle
class Water(Particle):
    def __init__(self, x, y):
        colours = [(20, 61, 247), (16, 72, 161), (14, 49, 204), (5, 74, 120), (19, 54, 212)]
        super().__init__(x, y, random.choice(colours))
        self.ID = 1
        self.NAME = "Water"
        self.GRAVITY = 0.3
        self.TERMINAL_VELOCITY = 1
        self.BUOYANCY = 1
        self.LIQUID = True

    def get_water_level(self, roi):
        waterLevels = np.sum(roi != 0, axis=0)  # Sum of non-zero elements in each column
        if len(waterLevels) > 0:
            return np.mean(waterLevels) 
        else:
            return 0

    # Used to move sand particles
    def move(self, newGrid, y, x, roi):
        CELLS_Y = len(newGrid) - 2
        CELLS_X = len(newGrid[0]) - 2

        # If can't move
        if np.all(roi[1:, :] != 0):
            self.velocity[0] = 0
            return newGrid

        # Update velocity (accelerate)
        self.velocity[0] += self.GRAVITY

        # Conform to terminal velocity
        if self.velocity[0] > self.TERMINAL_VELOCITY:
            self.velocity[0] = self.TERMINAL_VELOCITY

        newY = y + int(self.velocity[0])

        if newY >= CELLS_Y + 1:
            newY = CELLS_Y

        # If can fall straight down
        if roi[2, 1] == 0 and y < CELLS_Y:
            # Fall as far as velocity allows
            for i in range(newY, y, -1):
                if i < CELLS_Y - 1 and newGrid[i, x] == 0:
                    newGrid[i, x] = newGrid[y, x]
                    newGrid[y, x] = 0
                    self.y = i
                    return newGrid

            
        # If can move left
        elif roi[2, 0] == 0 and roi[2, 2] != 0 and x > 1 and y < CELLS_Y:
            if newGrid[y+1, x-1] == 0:
                newGrid[y+1, x-1] = newGrid[y, x]
                newGrid[y, x] = 0
                self.y += 1
                self.x -=1
        # If can move right
        elif roi[2, 2] == 0 and roi[2, 0] != 0 and x < CELLS_X and y < CELLS_Y:
            if newGrid[y+1, x+1] == 0:
                newGrid[y+1, x+1] = newGrid[y, x]
                newGrid[y, x] = 0
                self.y += 1
                self.x += 1
        # Stochastic movement if can move either direction
        elif roi[2, 2] == 0 and roi[2, 0] == 0 and y < CELLS_Y + 1:
            # Cant move right, move left
            if x == CELLS_X:
                if newGrid[y+1, x-1] == 0:
                    newGrid[y+1, x-1] = newGrid[y, x]
                    newGrid[y, x] = 0
                    self.y += 1
                    self.x -= 1
            # Cant move left, move right
            elif x == 1:
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

        # Move along its current height
        elif roi[1, 0] == 0 or roi[1, 2] == 0:
            # Water equalisation
            if CELLS_X - x <= 15:
                maxX = CELLS_X
            else: 
                maxX = x + 15
            
            if x - 15 < 1:
                minX = 0
            else: 
                minX = x - 15

            leftWaterRoi = newGrid[y-4:CELLS_Y-1, minX:x]
            rightWaterRoi = newGrid[y-4:CELLS_Y-1, x:maxX]
            leftLevel = self.get_water_level(leftWaterRoi)
            rightLevel = self.get_water_level(rightWaterRoi)

            if leftLevel < rightLevel and leftLevel < CELLS_Y - y:
                equalDirection = 0
            elif leftLevel > rightLevel and rightLevel < CELLS_Y - y:
                equalDirection = 1
            else:
                equalDirection = 2


            # Direction - 0 = left, 1 = right, 2 = neither
            direction = random.randint(0, 2)
            # Simulate water pressure, if free space left and water above, be pushed left
            if roi[1, 0] == 0 and ((roi[0, 1] != 0 and roi[0,2] != 0) or roi[0,2] != 0) and x > 1:
                if newGrid[y, x-1] == 0:
                    newGrid[y, x-1] = newGrid[y, x]
                    newGrid[y, x] = 0
                    self.x -= 1
            # Simulate water pressure, if free space left and water above, be pushed left
            elif roi[1, 2] == 0 and ((roi[0, 1] != 0 and roi[0,0] != 0) or roi[0,0] != 0) and x < CELLS_X:
                if newGrid[y, x+1] == 0:
                    newGrid[y, x+1] = newGrid[y, x]
                    newGrid[y, x] = 0
                    self.x += 1
            # If can only move left
            elif roi[1, 0] == 0 and roi[1, 2] != 0 and x > 1:
                if equalDirection == 0:
                    if newGrid[y, x-1] == 0:
                        newGrid[y, x-1] = newGrid[y, x]
                        newGrid[y, x] = 0
                        self.x -= 1
                elif direction == 0:
                    if newGrid[y, x-1] == 0:
                        newGrid[y, x-1] = newGrid[y, x]
                        newGrid[y, x] = 0
                        self.x -= 1
            # If can only move right
            elif roi[1, 0] != 0 and roi[1, 2] == 0 and x < CELLS_X:
                if equalDirection == 1:
                    if newGrid[y, x+1] == 0:
                        newGrid[y, x+1] = newGrid[y, x]
                        newGrid[y, x] = 0
                        self.x += 1
                elif direction == 1:
                    if newGrid[y, x+1] == 0:
                        newGrid[y, x+1] = newGrid[y, x]
                        newGrid[y, x] = 0
                        self.x += 1
            # If can move either way
            elif roi[1, 0] == 0 and roi[1, 2] == 0 :
                if equalDirection == 0 and x > 1:
                    if newGrid[y, x-1] == 0:
                        newGrid[y, x-1] = newGrid[y, x]
                        newGrid[y, x] = 0
                        self.x -= 1
                elif equalDirection == 1 and x < CELLS_X:
                    if newGrid[y, x+1] == 0:
                        newGrid[y, x+1] = newGrid[y, x]
                        newGrid[y, x] = 0
                        self.x += 1
                # Cant move right, possibly move left
                elif x == CELLS_X and direction == 0:
                        if newGrid[y, x-1] == 0:
                            newGrid[y, x-1] = newGrid[y, x]
                            newGrid[y, x] = 0
                            self.x -= 1
                # Cant move left, move right
                elif x == 1 and direction == 1:
                        if newGrid[y, x+1] == 0:
                            newGrid[y, x+1] = newGrid[y, x]
                            newGrid[y, x] = 0
                            self.x += 1
                else:
                    # Move left
                    if direction == 0 and x > 1:
                        if newGrid[y, x-1] == 0:
                            newGrid[y, x-1] = newGrid[y, x]
                            newGrid[y, x] = 0
                            self.x -= 1
                    # Move right
                    elif direction == 1 and x < CELLS_X:
                        if newGrid[y, x+1] == 0:
                            newGrid[y, x+1] = newGrid[y, x]
                            newGrid[y, x] = 0
                            self.x += 1

        return newGrid