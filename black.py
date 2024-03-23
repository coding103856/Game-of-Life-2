import pygame
import numpy as np
import random

# Define the size of the hexagonal grid
GRID_SIZE = 100
GRID_WIDTH = 800
GRID_HEIGHT = 600
CELL_SIZE = GRID_WIDTH // GRID_SIZE

# Define the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

# Define the grid
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        if random.random() < 0.7:
            grid[i, j] = 1

# Define the functions
def get_neighbors(grid, x, y):
    directions = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        while 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]:
            if grid[nx, ny] == 1:
                neighbors.append((nx, ny))
                break
            nx, ny = nx + dx, ny + dy
    return neighbors

def update_cell(grid, x, y):
    live_neighbors = get_neighbors(grid, x, y)
    if grid[x, y] == 1:
        if len(live_neighbors) < 2 or len(live_neighbors) > 3:
            return 0
    elif grid[x, y] == 0:
        if len(live_neighbors) == 3:
            return 1
    return grid[x, y]

def update_grid(grid):
    new_grid = np.zeros_like(grid)
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            new_grid[x, y] = update_cell(grid, x, y)
    return new_grid

def draw_grid(grid):
    screen.fill(WHITE)
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == 1:
                pygame.draw.rect(screen, BLACK, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update()

# Define the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the grid
    grid = update_grid(grid)

    # Draw the grid
    draw_grid(grid)

    # Set the frame rate
    clock.tick(2)

pygame.quit()