# maze.py

import random
from constants import GRID_HEIGHT, GRID_WIDTH

def generate_maze(height, width):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    def carve(cx, cy):
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 < nx < height and 0 < ny < width and maze[nx][ny] == 1:
                maze[cx + dx // 2][cy + dy // 2] = 0
                maze[nx][ny] = 0
                carve(nx, ny)

    maze[1][1] = 0
    carve(1, 1)
    return maze