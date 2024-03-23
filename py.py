import pygame
import numpy as np
import random

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 10
GENERATIONS = 100

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Define hexagonal grid directions
NEIGHBOR_DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, 1), (1, -1)]

def generate_hexagonal_grid(rows, cols):
    grid = np.zeros((rows, cols), dtype=int)
    return grid

def draw_hexagonal_grid(screen, grid):
    screen.fill(BLACK)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            color = GREEN if grid[i][j] == 1 else BLACK
            draw_hexagon(screen, (i, j), color)
    pygame.display.update()

def draw_hexagon(screen, pos, color):
    x, y = pos
    offset_x = x * 1.5 * CELL_SIZE
    offset_y = y * np.sqrt(3) * CELL_SIZE
    points = [(offset_x + CELL_SIZE, offset_y),
              (offset_x + 0.5 * CELL_SIZE, offset_y + np.sqrt(3) * 0.5 * CELL_SIZE),
              (offset_x - 0.5 * CELL_SIZE, offset_y + np.sqrt(3) * 0.5 * CELL_SIZE),
              (offset_x - CELL_SIZE, offset_y),
              (offset_x - 0.5 * CELL_SIZE, offset_y - np.sqrt(3) * 0.5 * CELL_SIZE),
              (offset_x + 0.5 * CELL_SIZE, offset_y - np.sqrt(3) * 0.5 * CELL_SIZE)]
    pygame.draw.polygon(screen, color, points, 0)

def count_live_neighbors(grid, row, col):
    count = 0
    for dr, dc in NEIGHBOR_DIRECTIONS:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
            count += grid[new_row][new_col]
    return count

def apply_rules(grid):
    new_grid = np.copy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            live_neighbors = count_live_neighbors(grid, i, j)
            if grid[i][j] == 1:  # If cell is alive
                if live_neighbors < 2:
                    new_grid[i][j] = 0  # Dies by underpopulation
                elif live_neighbors > 3:
                    new_grid[i][j] = 0  # Dies by overpopulation
            else:  # If cell is dead
                if live_neighbors == 3:
                    new_grid[i][j] = 1  # Resurrects
    return new_grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hexagonal Game of Life")

    rows = SCREEN_HEIGHT // (CELL_SIZE * int(np.sqrt(3)))
    cols = SCREEN_WIDTH // (int(1.5 * CELL_SIZE))

    grid = generate_hexagonal_grid(rows, cols)

    for _ in range(GENERATIONS):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        grid = apply_rules(grid)
        draw_hexagonal_grid(screen, grid)
        pygame.time.wait(100)  # Delay between generations

    pygame.quit()

if __name__ == "__main__":
    main()
