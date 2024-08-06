import pygame
import random
import sys
import heapq

from maze_defines import *

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
TILE_SIZE = SCREEN_WIDTH // MAP_SIZE  # Adjust for 20x20 maze
WHITE, BLACK, GREEN, RED, BLUE, LIGHT_RED, LIGHT_BLUE, PURPLE, LIGHT_PURPLE = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 200, 200), (200, 200, 255), (128, 0, 128), (200, 128, 200)

# Define a new navigable maze layout with a central goal
maze_layout = [
    [START, WALL, EMPTY, EMPTY, WALL, WALL, WALL, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, EMPTY, EMPTY, WALL, WALL],
    [EMPTY, WALL, WALL, EMPTY, WALL, EMPTY, WALL, EMPTY, WALL, EMPTY, WALL, WALL, EMPTY, WALL, EMPTY, WALL, WALL, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [WALL, WALL, WALL, EMPTY, WALL, EMPTY, WALL, WALL, WALL, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, WALL, WALL],
    [WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY],
    [WALL, EMPTY, WALL, WALL, WALL, WALL, WALL, WALL, EMPTY, WALL, WALL, WALL, EMPTY, EMPTY, WALL, WALL, WALL, WALL, WALL, EMPTY],
    [WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY],
    [WALL, WALL, WALL, WALL, WALL, EMPTY, WALL, WALL, WALL, WALL, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, WALL, WALL, WALL, WALL, WALL, EMPTY, EMPTY, EMPTY],
    [WALL, EMPTY, WALL, EMPTY, WALL, WALL, WALL, EMPTY, WALL, END, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
    [EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, EMPTY, WALL, WALL, WALL, EMPTY, EMPTY],
    [WALL, WALL, EMPTY, EMPTY, WALL, EMPTY, WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL],
    [EMPTY, WALL, EMPTY, WALL, WALL, EMPTY, EMPTY, WALL, WALL, EMPTY, WALL, WALL, WALL, WALL, WALL, WALL, EMPTY, WALL, EMPTY, EMPTY],
    [EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL, EMPTY],
    [EMPTY, WALL, WALL, WALL, EMPTY, EMPTY, WALL, EMPTY, WALL, WALL, EMPTY, WALL, WALL, WALL, WALL, WALL, EMPTY, WALL, EMPTY, EMPTY],
    [WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [WALL, EMPTY, WALL, EMPTY, WALL, EMPTY, WALL, WALL, EMPTY, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, EMPTY, WALL, EMPTY],
    [WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY],
    [WALL, WALL, WALL, WALL, WALL, WALL, EMPTY, WALL, WALL, WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, WALL, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, START]
]



# Maze class
class Maze:
    def __init__(self, layout):
        self.layout = layout

    def draw(self, screen, players):
        for i, row in enumerate(self.layout):
            for j, tile in enumerate(row):
                color = WHITE if tile == EMPTY else BLACK if tile == WALL else GREEN if tile == START else PURPLE if tile == END else WHITE
                pygame.draw.rect(screen, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        explored_by_both = set(players[0].explored_tiles) & set(players[1].explored_tiles)
        for player in players:
            for (x, y) in player.explored_tiles:
                if (x, y) in explored_by_both and self.layout[x][y] == EMPTY:
                    pygame.draw.rect(screen, LIGHT_PURPLE, (y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif self.layout[x][y] == EMPTY:
                    pygame.draw.rect(screen, player.explore_color, (y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Draw players on top of the explored tiles
        for player in players:
            x, y = player.position
            pygame.draw.rect(screen, player.color, (y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE))


# Player class
class Player:
    def __init__(self, start_pos, color, explore_color, decide_action):
        self.position = start_pos
        self.color = color
        self.explore_color = explore_color
        self.decide_action = decide_action
        self.known_map = [['?' for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]  # Update to 20x20
        self.previous_positions = []
        self.explored_tiles = set()

    def update_known_map(self, maze):
        x, y = self.position
        for i in range(max(0, x-1), min(MAP_SIZE, x+2)):  # Update range for 20x20
            for j in range(max(0, y-1), min(MAP_SIZE, y+2)):  # Update range for 20x20
                if 0 <= i < MAP_SIZE and 0 <= j < MAP_SIZE:  # Ensure indices are within bounds
                    self.known_map[i][j] = maze[i][j]
                    if maze[i][j] != WALL:
                        self.explored_tiles.add((i, j))

# Game class
class Game:
    def __init__(self, maze, players):
        self.maze = Maze(maze)
        self.players = players
        self.winner = None

    def move_player(self, player, direction):
        x, y = player.position
        if direction == 'up' and x > 0 and self.maze.layout[x-1][y] != WALL:
            player.position = (x-1, y)
        elif direction == 'down' and x < MAP_SIZE-1 and self.maze.layout[x+1][y] != WALL:  # Update for 20x20
            player.position = (x+1, y)
        elif direction == 'left' and y > 0 and self.maze.layout[x][y-1] != WALL:
            player.position = (x, y-1)
        elif direction == 'right' and y < MAP_SIZE-1 and self.maze.layout[x][y+1] != WALL:  # Update for 20x20
            player.position = (x, y+1)

    def check_winner(self):
        for player in self.players:
            if self.maze.layout[player.position[0]][player.position[1]] == END:
                self.winner = player
                return True
        return False

    def update_players(self):
        for player in self.players:
            player.previous_positions.append(player.position)
            player.update_known_map(self.maze.layout)

    def run(self):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Maze Game')

        clock = pygame.time.Clock()
        running = True

        while running:
            screen.fill(BLACK)
            self.maze.draw(screen, self.players)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not self.winner:
                for player in self.players:
                    action = player.decide_action(player.position, player.previous_positions, player.known_map)
                    self.move_player(player, action)
                    self.update_players()
                    if self.check_winner():
                        print(f'Player {self.players.index(player) + 1} wins!')
                        running = False
                        break

            clock.tick(5)

        pygame.quit()
        sys.exit()



def a_star_algorithm(start, goal, known_map):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    def get_neighbors(pos):
        neighbors = []
        x, y = pos
        for move in ['up', 'down', 'left', 'right']:
            nx, ny = x, y
            if move == 'up':
                nx -= 1
            elif move == 'down':
                nx += 1
            elif move == 'left':
                ny -= 1
            elif move == 'right':
                ny += 1
            if 0 <= nx < MAP_SIZE and 0 <= ny < MAP_SIZE and known_map[nx][ny] != WALL:
                neighbors.append((nx, ny, move))
        return neighbors

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                current, move = came_from[current]
                path.append(move)
            return path[::-1]  # Reverse the path

        for nx, ny, move in get_neighbors(current):
            neighbor = (nx, ny)
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                came_from[neighbor] = (current, move)

    return []  # Return an empty path if no path found

def player1_algorithm(current_pos, previous_positions, known_map):
    goal_pos = GOAL_POSITION  # Position of the END tile
    path = a_star_algorithm(current_pos, goal_pos, known_map)
    if path:
        next_move = path[0]
        if next_move == 'up':
            return 'up'
        elif next_move == 'down':
            return 'down'
        elif next_move == 'left':
            return 'left'
        elif next_move == 'right':
            return 'right'
    return random.choice(['up', 'down', 'left', 'right'])

def player2_algorithm(current_pos, previous_positions, known_map):
    goal_pos = (5, 5)  # Position of the END tile
    path = a_star_algorithm(current_pos, goal_pos, known_map)
    if path:
        return path[0]
    return random.choice(['up', 'down', 'left', 'right'])



# Initialize players with their respective algorithms and game
players = [Player((0, 0), RED, LIGHT_RED, player1_algorithm), Player((19, 19), BLUE, LIGHT_BLUE, player2_algorithm)]
game = Game(maze_layout, players)
game.run()

