# Powder Toy Clone - A Simple Physics Simulation

---

## Overview

**Powder Toy Clone** is a basic simulation of a powder-like substance that reacts to gravity and interacts with its surroundings. Built using Python and Pygame, this project provides a sandbox environment where users can experiment with the behavior of particles and observe their interactions in real-time. This project serves as a learning tool for understanding physics simulations, particle dynamics, and game development.

This project is based on the game [Powder Toy](https://powdertoy.co.uk/)[^1], and intends to implement the basic features such as solids and liquids. This readme will be updated after each major feature addition, which will be chronicled [Development](#development).

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Customization](#customization)
5. [Development](#development)
    - [21/08/24 - Adding basic controls and movement](#210824---adding-basic-controls-and-movement)
    - [22/08/24 - Encapsulating functionality into classes](#220824---encapsulating-functionality-into-classes)
6. [License](#license)
7. [References](#references)

---

## Features

- **Interactive Grid:**
  - Use the mouse to draw particles on the grid.
  - Particles fall under gravity and interact with their environment.
- **Keyboard Controls:**
  - **Space:** Pause and resume the simulation.
  - **C:** Clear the entire grid.
  - **Q:** Quit the game.
- **Real-time Simulation:**
  - Observe the particles' behavior in real-time as they interact with each other and their environment.

---

## Installation

To run this project, you will need Python 3.6 or higher and the following Python packages:

- `numpy`
- `pygame`

You can install these dependencies using pip:

```sh
pip install numpy pygame
```

To start the simulation, run the following command:

```sh
python game.py
```

---

## Usage

### Playing the Game:

- The simulation starts with an empty grid. Use the keyboard shortcuts to control the game.
- Left-click to draw particles and right-click to erase them.
- The simulation applies gravity to particles, causing them to fall and interact with their surroundings.

### Keyboard Shortcuts:

- **Pause/Resume**: Press `Space` to pause and unpause the simulation.
- **Clear Grid**: Press `C` to clear all particles on the grid.
- **Quit**: Press `Q` to exit the game.

---

## Customization

You can customize various aspects of the game, such as:

- **Resolution**: Adjust the `RESOLUTION` variable to change the size of the cells.
- **Window Size**: Adjust the `WIDTH`, `HEIGHT`, and `GAMEWIDTH` variables to change the size of the window. You may also need to adjust the positions of text fields accordingly.
- **Game Speed**: Modify the `FPS` variable to change the speed of the simulation.
- **Colors**: Customize the colors of the particles in the `colours` variable.

---

## Development

### 21/08/24 - Adding basic controls and movement

Today I first began creating my version of Powder Toy. I was able to reuse code from my **Game of Life**[^2] project to get the basic window to appear, and to draw a particle to the screen. From here, I began to implement the basic movement logic for a single particle.

```python
def move_sand(y, x, roi, newGrid):
    if y < CELLS_Y - 1:
        # If can fall straight down
        if roi[2, 1] == 0:
            print(newGrid[y, x])
            print(newGrid[y+1, x])
            newGrid[y+1, x] = newGrid[y, x]
            newGrid[y, x] = 0
        # If can fall left
        elif np.array_equal(roi[2], [0, 1, 1]) and x > 0:
            newGrid[y+1, x-1] = newGrid[y, x]
            newGrid[y, x] = 0
        # If can fall right
        elif np.array_equal(roi[2], [1, 1, 0]) and x < CELLS_X - 1:
            newGrid[y+1, x+1] = newGrid[y, x]
            newGrid[y, x] = 0
        # Stochastic movement if the sand can move either left or right
        elif np.array_equal(roi[2], [0, 1, 0]):
            # If can't move left, move right
            if x == 0:
                newGrid[y+1, x+1] = newGrid[y, x]
                newGrid[y, x] = 0
            # If can't move right, move left
            elif x == CELLS_X - 1:
                newGrid[y+1, x-1] = newGrid[y, x]
                newGrid[y, x] = 0
            # Otherwise, random direction
            else:
                direction = random.randint(0, 1)
                # Move left
                if direction == 0:
                    newGrid[y+1, x-1] = newGrid[y, x]
                    newGrid[y, x] = 0
                else:
                    newGrid[y+1, x+1] = newGrid[y, x]
                    newGrid[y, x] = 0
```


The above logic checks within a 3x3 region of interest, centred on the pixel we intend to move. The row of pixels directly below the current pixel are checked, and if the row conforms to one of 4 different conditions, the particle will move, otherwise will stay in place. This logic is very simple, and so once tested I quickly moved on to adding gravity and velocity. 

To implement gravity, I added a new array in which the velocity of each cell is stored. Every iteration, the velocity is increased by the gravity value (which is 0.7), and is clamped at a maximum velocity of 3. These values were find via trial and error, trying to find what appeared to my eyes to be the best.

During the process of adding velocity, I also took a slight detour to add colour to the game. Another array contains each pixel's colour, and is updated in the same way as the velocity during movement, as shown in the following example:

```python
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
  .....
```


To give a particle a colour, the colour array is checked. If the particles position in the colour array is set to 0, a new colour is assigned to that index, which is then moved whenever the particle moves. The available colours for each material is stored in an array within a dictionary, which is accessed through indexing the dictionary using the material ID (e.g. Sand has an ID of 1)

```python
# Dictionary to hold colour values
colours = {
    "0": [(0, 0, 0)],
    # Sand
    "1": [(117, 108, 30), (156, 113, 28), (181, 128, 22), (153, 126, 20), (140, 114, 13)]
           }
...
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
```


These changes produced the following results:

![Basic Falling Sand](gifs/sandFall.gif)


The final change I made to the initial version of this project was to add a set of controls. I added the ability to add and remove particles of sand, as well as clear the grid of any particles. This was done by polling input events and either setting a flag to `True` or `False` to denote which mouse button was pressed, or calling a function to perform the intended action. 

```python
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

...

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

```


With these changes, the first version of the game was complete, and the game functioned as intended.

![Basic Controls](gifs/mouse_controls.gif)


For the next step of development, I intend to add a basic fluid simulation, and will then test the combination of solid and liquid materials.

<br>

### 22/08/24 - Encapsulating functionality into classes

In order to improve readability, maintainability, and ease of addition of new features, I have encapsulated the game into several classes. The main game now exists in a `PowderToy` class within `game.py`. This class contains the attributes that control the pygame window, as well as the main game loop. 

The logic for particles now exists within the `particles` package. A superclass `Particle` exists to store the basic particle information. Currently, the only particle is sand, which also exists in its own `Sand` class within `particles/Sand.py`. Future particles will have their own classes and files, as with Sand. All functionality for a particle exists within its class. Currently, particle classes contain:

- **Attributes:**
    - **x:** The particle's x position within the game grid.
    - **y:** The particle's y position within the game grid.
    - **colour:** The particles colour in (r, g, b)
    - **velocity:** The particles velocity, stored as a 2d vector of (y x)
    - **NAME:** The name of the particle.
    - **GRAVITY:** How much the particle is affected by gravity.
    - **TERMINAL_VELOCITY:** The maximum speed a particle is allowed to fall.
- **Methods:**
    - **move:** Handles the movement logic for the particle. Will behave differently depending on the particle type.
    - **draw:** Draws the particle
 
As of writing this, the conversion from use of code in a single file and use of classes is not complete. I intended to replace the use of velocityGrid with just the velocity attribute, and intend to replace the draw function as written in the movement handling in the `PowderToy` class with a call to the particle's draw function.

---
## License

Feel free to use, modify, and distribute this code as needed. The author of this project is Lewis Murphy, @defalt0402. If you have any questions or need further clarification, please reach out!

---

## References

[^1]: [Original Powder Toy Github](https://github.com/The-Powder-Toy/The-Powder-Toy): The Github page of the original powder toy game.
[^2]: [Conways Game of Life](https://github.com/Defalt0402/Conways-game-of-life): My implementation of Conway's Game of Life
