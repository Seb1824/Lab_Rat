# maze.py

import random
from constants import GRID_HEIGHT, GRID_WIDTH

def generate_maze():
    rows = GRID_HEIGHT  # debe ser impar
    maze = [[1 for _ in range(rows)] for _ in range(rows)]

    def carve_passages_from(cx, cy):
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx*2, cy + dy*2
            if 0 <= nx < rows and 0 <= ny < rows and maze[nx][ny] == 1:
                maze[cx + dx][cy + dy] = 0
                maze[nx][ny] = 0
                carve_passages_from(nx, ny)

    maze[1][1] = 0
    carve_passages_from(1, 1)
    return maze
