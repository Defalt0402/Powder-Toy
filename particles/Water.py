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

    def get_water_level(self, roi):
        waterLevels = np.sum(roi != 0, axis=0)  # Sum of non-zero elements in each column
        if len(waterLevels) > 0:
            return np.mean(waterLevels) 
        else:
            return 0

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
        b, bl, br, l, r = False, False, False, False, False
        if y < CELLS_Y - 1:
            if newGrid[y+1, x] == 0:
                b = True
            if x > 0 and newGrid[y+1, x-1] == 0:
                bl = True
            if x < CELLS_X - 1 and newGrid[y+1, x+1] == 0:
                br = True
        if x > 0 and newGrid[y, x-1] == 0:
            l = True
        if x < CELLS_X - 1 and newGrid[y, x+1] == 0:
            r = True
        
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
            # spreadRange = 2
            # # Water equalisation
            # maxX = min(CELLS_X - 1, x + 15)
            # minX = max(0, x - 15)

            # leftWaterRoi = newGrid[y-4:CELLS_Y-1, minX:x]
            # rightWaterRoi = newGrid[y-4:CELLS_Y-1, x:maxX]
            # leftLevel = self.get_water_level(leftWaterRoi)
            # rightLevel = self.get_water_level(rightWaterRoi)

            # # If water is lower on the left, and is lower than current particle
            # if leftLevel < rightLevel and leftLevel < y - 1:
            #     for j in range(1, spreadRange +1):
            #         # If as far as possible without problem
            #         if x - j == -1 and newGrid[y, x - j + 1] == 0:
            #             newGrid[y, x - j + 1] = newGrid[y, x]
            #             newGrid[y, x] = 0
            #             self.x -= (j + 1)
            #             return newGrid
            #         elif x + j == -1:
            #             return newGrid
            #         elif newGrid[y, x - j] == 0 and j == spreadRange:
            #             newGrid[y, x - j] = newGrid[y, x]
            #             newGrid[y, x] = 0
            #             self.x -= j
            #             return newGrid
            #         # If reach obstacle, but free space before
            #         elif newGrid[y, x - j] != 0 and newGrid[y, x - j + 1] == 0:
            #             newGrid[y, x - j + 1] = newGrid[y, x]
            #             newGrid[y, x] = 0
            #             self.x -= (j + 1)
            #             return newGrid
            # # If water is lower on the right and lowwer than current particle
            # elif rightLevel < leftLevel and rightLevel < y - 1:
            #     for j in range(1, spreadRange +1):
            #         # If as far as possible without problem
            #         if x + j == CELLS_X and newGrid[y, x + j - 1] == 0:
            #             newGrid[y, x + j - 1] = newGrid[y, x]
            #             newGrid[y, x] = 0
            #             self.x += j
            #             return newGrid
            #         elif x + j == CELLS_X:
            #             return newGrid
            #         elif newGrid[y, x + j] == 0 and j == spreadRange:
            #             newGrid[y, x + j] = newGrid[y, x]
            #             newGrid[y, x] = 0
            #             self.x += j
            #             return newGrid
            #         # If reach obstacle, but free space before
            #         elif newGrid[y, x + j] != 0 and newGrid[y, x + j - 1] == 0:
            #             newGrid[y, x + j - 1] = newGrid[y, x]
            #             newGrid[y, x] = 0
            #             self.x += (j - 1)
            #             return newGrid
            
            if l and not r:
                newGrid[y, x-1] = newGrid[y, x]
                newGrid[y, x] = 0
                self.x -=1
                return newGrid
            elif r and not l:
                newGrid[y, x+1] = newGrid[y, x]
                newGrid[y, x] = 0
                self.x +=1
                return newGrid
            elif r and l:
                direction = random.randint(0, 1)
                # Move left
                if direction == 0:
                    newGrid[y, x-1] = newGrid[y, x]
                    newGrid[y, x] = 0
                    self.x -=1
                    return newGrid
                # Move right
                else:
                    newGrid[y, x+1] = newGrid[y, x]
                    newGrid[y, x] = 0
                    self.x +=1
                    return newGrid
                
        return newGrid