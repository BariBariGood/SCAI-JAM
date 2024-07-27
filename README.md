# SCAI-JAM

A Pygame-based maze game where two players navigate a 20x20 maze with an invisible border to prevent them from moving out of bounds. The players use A* pathfinding algorithms to find the shortest path to the goal.

## Features

- Two players with different colors and exploration trails.
- A* pathfinding algorithm for smart and efficient navigation.
- Invisible border to ensure players do not move out of bounds.
- Visualization of explored tiles and player positions.

## Installation

1. Ensure you have Python installed on your machine.
2. Install Pygame using pip:
    ```sh
    pip install pygame
    ```

## Usage

1. Clone the repository or download the script.
2. Run the game:
    ```sh
    python game.py
    ```

## Maze Layout

The maze layout is a 20x20 grid with an invisible border, making it effectively a 22x22 grid. The edges are treated as solid walls to prevent players from moving out of bounds.

### Example Layout
```python
maze_layout = [
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
    [WALL, START, WALL, EMPTY, EMPTY, WALL, WALL, WALL, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, EMPTY, WALL, WALL, WALL],
    [WALL, EMPTY, WALL, WALL, EMPTY, WALL, EMPTY, WALL, EMPTY, WALL, EMPTY, WALL, WALL, EMPTY, WALL, EMPTY, WALL, WALL, EMPTY, WALL, WALL],
    [WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL],
    [WALL, WALL, WALL, EMPTY, WALL, EMPTY, WALL, WALL, WALL, WALL, EMPTY, WALL, WALL, EMPTY, EMPTY, WALL, WALL, EMPTY, WALL, WALL, WALL],
    [WALL, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, WALL, EMPTY, EMPTY, WALL, WALL],
    [WALL, WALL, EMPTY, WALL, WALL, WALL, END, WALL, WALL, EMPTY, WALL, WALL, WALL, EMPTY, EMPTY, WALL, WALL, WALL, WALL, WALL, WALL],
    [WALL, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL],
    [WALL, WALL, WALL, WALL, WALL, EMPTY, WALL, WALL, WALL, WALL, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, WALL, WALL],
    [WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, WALL, WALL, WALL, WALL, WALL, EMPTY, EMPTY, WALL, WALL],
    [WALL, EMPTY, WALL, EMPTY, WALL, WALL, WALL, EMPTY, WALL, START, EMPTY, WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL],
    [WALL, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, EMPTY, WALL, WALL, WALL, WALL, WALL],
    [WALL, WALL, EMPTY, EMPTY, WALL, EMPTY, WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL],
    [WALL, EMPTY, WALL, EMPTY, WALL, WALL, EMPTY, WALL, WALL, WALL, EMPTY, WALL, WALL, WALL, WALL, WALL, EMPTY, WALL, EMPTY, WALL, WALL],
    [WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, WALL],
    [WALL, EMPTY, WALL, WALL, WALL, WALL, EMPTY, WALL, WALL, EMPTY, WALL, WALL, WALL, WALL, WALL, WALL, WALL, EMPTY, WALL, WALL, WALL],
    [WALL, WALL, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL],
    [WALL, WALL, EMPTY, WALL, EMPTY, WALL, EMPTY, WALL, WALL, EMPTY, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
    [WALL, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL],
    [WALL, WALL, WALL, WALL, WALL, WALL, EMPTY, WALL, WALL, WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, EMPTY, WALL, WALL],
    [WALL, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL],
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL]
]
