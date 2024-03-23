#include <SFML/Graphics.hpp>
#include <vector>
#include <iostream>
#include <cstdlib>
#include <ctime>

// Define constants
const int SCREEN_WIDTH = 800;
const int SCREEN_HEIGHT = 600;
const int CELL_SIZE = 10;
const int ROWS = SCREEN_HEIGHT / (CELL_SIZE * 2);
const int COLS = SCREEN_WIDTH / (CELL_SIZE * 1.5);
const int GENERATIONS = 100;

// Define colors
const sf::Color WHITE = sf::Color::White;
const sf::Color BLACK = sf::Color::Black;
const sf::Color GREEN = sf::Color::Green;

// Define hexagonal grid directions
const std::vector<std::pair<int, int>> NEIGHBOR_DIRECTIONS = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}, {-1, 1}, {1, -1}};

// Function to initialize the hexagonal grid
std::vector<std::vector<int>> generateHexagonalGrid() {
    std::vector<std::vector<int>> grid(ROWS, std::vector<int>(COLS, 0));
    return grid;
}

// Function to draw a hexagon
void drawHexagon(sf::RenderWindow& window, int x, int y, sf::Color color) {
    sf::ConvexShape hexagon;
    hexagon.setPointCount(6);
    for (int i = 0; i < 6; ++i) {
        float angle = 60 * i + 30;
        float radians = 3.14159 * angle / 180.0;
        hexagon.setPoint(i, sf::Vector2f(x + CELL_SIZE * std::cos(radians), y + CELL_SIZE * std::sin(radians)));
    }
    hexagon.setFillColor(color);
    window.draw(hexagon);
}

// Function to count live neighbors
int countLiveNeighbors(const std::vector<std::vector<int>>& grid, int row, int col) {
    int count = 0;
    for (const auto& dir : NEIGHBOR_DIRECTIONS) {
        int newRow = row + dir.first;
        int newCol = col + dir.second;
        if (newRow >= 0 && newRow < ROWS && newCol >= 0 && newCol < COLS) {
            count += grid[newRow][newCol];
        }
    }
    return count;
}

// Function to apply the modified rules
std::vector<std::vector<int>> applyRules(const std::vector<std::vector<int>>& grid) {
    std::vector<std::vector<int>> newGrid = grid;
    for (int i = 0; i < ROWS; ++i) {
        for (int j = 0; j < COLS; ++j) {
            int liveNeighbors = countLiveNeighbors(grid, i, j);
            if (grid[i][j] == 1) {  // If cell is alive
                if (liveNeighbors < 2) {
                    newGrid[i][j] = 0;  // Dies by underpopulation
                } else if (liveNeighbors > 3) {
                    newGrid[i][j] = 0;  // Dies by overpopulation
                }
            } else {  // If cell is dead
                if (liveNeighbors == 3) {
                    newGrid[i][j] = 1;  // Resurrects
                }
            }
        }
    }
    return newGrid;
}

// Function to draw the hexagonal grid
void drawGrid(sf::RenderWindow& window, const std::vector<std::vector<int>>& grid) {
    window.clear(BLACK);
    for (int i = 0; i < ROWS; ++i) {
        for (int j = 0; j < COLS; ++j) {
            sf::Color color = (grid[i][j] == 1) ? GREEN : BLACK;
            int xOffset = j * 1.5 * CELL_SIZE;
            int yOffset = i * CELL_SIZE * 2;
            if (i % 2 != 0) {
                xOffset += 0.75 * CELL_SIZE;
            }
            drawHexagon(window, xOffset, yOffset, color);
        }
    }
    window.display();
}

int main() {
    srand(time(nullptr));

    sf::RenderWindow window(sf::VideoMode(SCREEN_WIDTH, SCREEN_HEIGHT), "Hexagonal Game of Life");

    std::vector<std::vector<int>> grid = generateHexagonalGrid();

    for (int generation = 0; generation < GENERATIONS; ++generation) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
                return 0;
            }
        }

        grid = applyRules(grid);
        drawGrid(window, grid);

        sf::sleep(sf::milliseconds(100));  // Delay between generations
    }

    return 0;
}
